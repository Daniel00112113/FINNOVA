using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using FinancialCopilot.Application.Common.Interfaces;
using FinancialCopilot.Application.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace FinancialCopilot.Infrastructure.Services;

public class AiService : IAiService
{
    private readonly IApplicationDbContext _context;
    private readonly HttpClient _httpClient;
    private readonly string _aiEngineUrl;

    public AiService(IApplicationDbContext context, IConfiguration configuration, HttpClient httpClient)
    {
        _context = context;
        _httpClient = httpClient;
        _aiEngineUrl = configuration["AiEngine:Url"] ?? "http://localhost:8000";
    }

    public async Task<BalancePredictionDto> PredictBalanceAsync(Guid userId, int monthsAhead = 3)
    {
        var transactions = await GetUserTransactions(userId);
        
        var request = new
        {
            user_id = userId.ToString(),
            transactions = transactions.Select(t => new
            {
                amount = t.Amount,
                date = t.Date.ToString("o"),
                type = t.Type,
                category = t.Category
            }),
            months_ahead = monthsAhead
        };

        var response = await PostToAiEngine("/predict/balance", request);
        var result = JsonSerializer.Deserialize<AiBalancePredictionResponse>(response, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        });

        if (result == null)
            throw new Exception("Failed to get prediction from AI engine");

        return new BalancePredictionDto(
            result.Predictions.Select(p => new MonthlyPrediction(p.Month, (decimal)p.PredictedBalance, p.Confidence)).ToList(),
            result.Confidence,
            result.Trend,
            result.RiskLevel,
            result.Recommendations,
            (decimal)result.CurrentBalance
        );
    }

    public async Task<ExpensePredictionDto> PredictExpensesAsync(Guid userId, int monthsAhead = 3)
    {
        var transactions = await GetUserTransactions(userId);
        
        var request = new
        {
            user_id = userId.ToString(),
            transactions = transactions.Where(t => t.Type == "expense").Select(t => new
            {
                amount = t.Amount,
                date = t.Date.ToString("o"),
                type = t.Type,
                category = t.Category
            }),
            months_ahead = monthsAhead
        };

        var response = await PostToAiEngine("/predict/expenses", request);
        var result = JsonSerializer.Deserialize<AiExpensePredictionResponse>(response, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        });

        if (result == null)
            throw new Exception("Failed to get expense prediction from AI engine");

        var categoryPredictions = result.CategoryPredictions.ToDictionary(
            kvp => kvp.Key,
            kvp => new CategoryPrediction(
                (decimal)kvp.Value.Average,
                (decimal)kvp.Value.PredictedNextMonth,
                kvp.Value.Trend
            )
        );

        return new ExpensePredictionDto(categoryPredictions);
    }

    public async Task<SimulationResultDto> SimulateScenarios(Guid userId, int months = 12)
    {
        try
        {
            // Ejecutar consultas secuencialmente para evitar problemas de concurrencia
            var incomes = await _context.Incomes
                .Where(i => i.UserId == userId)
                .Select(i => new { i.Amount, i.Date })
                .ToListAsync();

            var expenses = await _context.Expenses
                .Where(e => e.UserId == userId)
                .Select(e => new { e.Amount, e.Date })
                .ToListAsync();

            var debts = await _context.Debts
                .Where(d => d.UserId == userId)
                .Select(d => new { d.RemainingAmount, d.InterestRate })
                .ToListAsync();

            var totalIncome = incomes.Sum(i => i.Amount);
            var totalExpenses = expenses.Sum(e => e.Amount);
            var totalDebt = debts.Sum(d => d.RemainingAmount);
            var avgInterestRate = debts.Where(d => d.RemainingAmount > 0).Average(d => (double?)d.InterestRate) ?? 0;

            var balance = totalIncome - totalExpenses;

            // Calcular promedios mensuales
            var monthCount = incomes.Select(i => i.Date.Month).Distinct().Count();
            monthCount = Math.Max(monthCount, 1);

            var monthlyIncome = totalIncome / monthCount;
            var monthlyExpenses = totalExpenses / monthCount;

            var request = new
            {
                current_balance = balance,
                monthly_income = monthlyIncome,
                monthly_expenses = monthlyExpenses,
                debt = totalDebt,
                interest_rate = avgInterestRate,
                months = months
            };

            Console.WriteLine($"Simulator Request: balance={balance}, income={monthlyIncome}, expenses={monthlyExpenses}");

            var response = await PostToAiEngine("/simulate", request);
            
            Console.WriteLine($"Simulator Response: {response.Substring(0, Math.Min(500, response.Length))}...");

            var result = JsonSerializer.Deserialize<AiSimulationResponse>(response, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (result == null)
                throw new Exception("Failed to deserialize simulation response from AI engine");

            if (result.Scenarios == null || result.Scenarios.Count == 0)
                throw new Exception("AI engine returned empty scenarios");

            Console.WriteLine($"Deserialized scenarios count: {result.Scenarios.Count}");
            Console.WriteLine($"Current scenario final balance: {result.Scenarios["current"].FinalBalance}");

            var scenarios = result.Scenarios.ToDictionary(
                kvp => kvp.Key,
                kvp => new ScenarioResult(
                    kvp.Value.Timeline.Select(t => new MonthlySnapshot(t.Month, (decimal)t.Balance, (decimal)t.Debt, (decimal)t.NetIncome)).ToList(),
                    (decimal)kvp.Value.FinalBalance,
                    (decimal)kvp.Value.FinalDebt,
                    (decimal)kvp.Value.TotalSaved,
                    (decimal)kvp.Value.TotalInterestPaid,
                    kvp.Value.DebtPaidOff,
                    kvp.Value.MonthsToPositive
                )
            );

            Console.WriteLine($"Converted current scenario final balance: {scenarios["current"].FinalBalance}");

            var comparisonScores = new Dictionary<string, ScenarioScore>();
            
            foreach (var kvp in result.Comparison)
            {
                // Skip "best_scenario" ya que es un string, no un objeto
                if (kvp.Key == "best_scenario")
                    continue;
                
                // Deserializar el JsonElement a AiScenarioScore
                var scoreData = JsonSerializer.Deserialize<AiScenarioScore>(kvp.Value.GetRawText(), new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
                
                if (scoreData != null)
                {
                    comparisonScores[kvp.Key] = new ScenarioScore(
                        (decimal)scoreData.FinalBalance,
                        (decimal)scoreData.FinalDebt,
                        (decimal)scoreData.Score,
                        scoreData.DebtPaidOff
                    );
                }
            }

            var comparison = new ScenarioComparison(comparisonScores, result.BestScenario);

            return new SimulationResultDto(
                scenarios,
                comparison,
                result.BestScenario,
                result.Recommendations
            );
        }
        catch (Exception ex)
        {
            Console.WriteLine($"SimulateScenarios Error: {ex.Message}");
            Console.WriteLine($"Stack: {ex.StackTrace}");
            throw;
        }
    }

    public async Task<RiskAnalysisDto> AnalyzeRiskAsync(Guid userId)
    {
        var transactions = await GetUserTransactions(userId);
        
        var request = new
        {
            user_id = userId.ToString(),
            transactions = transactions.Select(t => new
            {
                amount = t.Amount,
                date = t.Date.ToString("o"),
                type = t.Type
            }),
            months_ahead = 3
        };

        var response = await PostToAiEngine("/analyze/risk", request);
        var result = JsonSerializer.Deserialize<AiRiskAnalysisResponse>(response, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        });

        if (result == null)
            throw new Exception("Failed to get risk analysis from AI engine");

        return new RiskAnalysisDto(
            result.RiskScore,
            result.RiskLevel,
            result.Factors,
            result.Recommendations,
            new RiskMetrics(
                result.Metrics.ExpenseRatio,
                result.Metrics.Volatility,
                (decimal)result.Metrics.Balance
            )
        );
    }

    private async Task<List<TransactionData>> GetUserTransactions(Guid userId)
    {
        // Ejecutar consultas secuencialmente para evitar problemas de concurrencia
        var incomes = await _context.Incomes
            .Where(i => i.UserId == userId)
            .Select(i => new TransactionData
            {
                Amount = (double)i.Amount,
                Date = i.Date,
                Type = "income",
                Category = i.Type
            })
            .ToListAsync();

        var expenses = await _context.Expenses
            .Where(e => e.UserId == userId)
            .Select(e => new TransactionData
            {
                Amount = (double)e.Amount,
                Date = e.Date,
                Type = "expense",
                Category = e.Category
            })
            .ToListAsync();

        return incomes.Concat(expenses).OrderBy(t => t.Date).ToList();
    }

    private async Task<string> PostToAiEngine(string endpoint, object data)
    {
        try
        {
            var json = JsonSerializer.Serialize(data);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            
            Console.WriteLine($"Calling AI Engine: {_aiEngineUrl}{endpoint}");
            
            var response = await _httpClient.PostAsync($"{_aiEngineUrl}{endpoint}", content);
            response.EnsureSuccessStatusCode();
            
            return await response.Content.ReadAsStringAsync();
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"AI Engine not available: {ex.Message}");
            Console.WriteLine($"Using fallback mock data for endpoint: {endpoint}");
            
            // Fallback: devolver datos simulados cuando el AI Engine no está disponible
            return GetMockResponse(endpoint, data);
        }
    }
    
    private string GetMockResponse(string endpoint, object data)
    {
        return endpoint switch
        {
            "/simulate" => @"{
                ""scenarios"": {
                    ""current"": {
                        ""timeline"": [
                            {""month"": 1, ""balance"": 1000, ""debt"": 0, ""net_income"": 500},
                            {""month"": 2, ""balance"": 1500, ""debt"": 0, ""net_income"": 500},
                            {""month"": 3, ""balance"": 2000, ""debt"": 0, ""net_income"": 500}
                        ],
                        ""final_balance"": 2000,
                        ""final_debt"": 0,
                        ""total_saved"": 1500,
                        ""total_interest_paid"": 0,
                        ""debt_paid_off"": true,
                        ""months_to_positive"": 1
                    },
                    ""optimistic"": {
                        ""timeline"": [
                            {""month"": 1, ""balance"": 1200, ""debt"": 0, ""net_income"": 600},
                            {""month"": 2, ""balance"": 1800, ""debt"": 0, ""net_income"": 600},
                            {""month"": 3, ""balance"": 2400, ""debt"": 0, ""net_income"": 600}
                        ],
                        ""final_balance"": 2400,
                        ""final_debt"": 0,
                        ""total_saved"": 1800,
                        ""total_interest_paid"": 0,
                        ""debt_paid_off"": true,
                        ""months_to_positive"": 1
                    },
                    ""pessimistic"": {
                        ""timeline"": [
                            {""month"": 1, ""balance"": 800, ""debt"": 0, ""net_income"": 400},
                            {""month"": 2, ""balance"": 1200, ""debt"": 0, ""net_income"": 400},
                            {""month"": 3, ""balance"": 1600, ""debt"": 0, ""net_income"": 400}
                        ],
                        ""final_balance"": 1600,
                        ""final_debt"": 0,
                        ""total_saved"": 1200,
                        ""total_interest_paid"": 0,
                        ""debt_paid_off"": true,
                        ""months_to_positive"": 1
                    }
                },
                ""comparison"": {
                    ""current"": {""final_balance"": 2000, ""final_debt"": 0, ""score"": 75, ""debt_paid_off"": true},
                    ""optimistic"": {""final_balance"": 2400, ""final_debt"": 0, ""score"": 85, ""debt_paid_off"": true},
                    ""pessimistic"": {""final_balance"": 1600, ""final_debt"": 0, ""score"": 65, ""debt_paid_off"": true}
                },
                ""best_scenario"": ""optimistic"",
                ""recommendations"": [
                    ""AI Engine is currently unavailable - showing estimated data"",
                    ""Continue monitoring your expenses"",
                    ""Consider increasing your savings rate""
                ]
            }",
            _ => @"{""error"": ""AI Engine unavailable"", ""message"": ""Using fallback data""}"
        };
    }

    private class TransactionData
    {
        public double Amount { get; set; }
        public DateTime Date { get; set; }
        public string Type { get; set; } = string.Empty;
        public string? Category { get; set; }
    }

    private class AiBalancePredictionResponse
    {
        public List<AiMonthlyPrediction> Predictions { get; set; } = new();
        public double Confidence { get; set; }
        public string Trend { get; set; } = string.Empty;
        public string RiskLevel { get; set; } = string.Empty;
        public List<string> Recommendations { get; set; } = new();
        public double CurrentBalance { get; set; }
    }

    private class AiMonthlyPrediction
    {
        public string Month { get; set; } = string.Empty;
        public double PredictedBalance { get; set; }
        public double Confidence { get; set; }
    }

    private class AiExpensePredictionResponse
    {
        public Dictionary<string, AiCategoryPrediction> CategoryPredictions { get; set; } = new();
    }

    private class AiCategoryPrediction
    {
        public double Average { get; set; }
        public double PredictedNextMonth { get; set; }
        public string Trend { get; set; } = string.Empty;
    }

    private class AiSimulationResponse
    {
        [JsonPropertyName("scenarios")]
        public Dictionary<string, AiScenarioResult> Scenarios { get; set; } = new();
        
        [JsonPropertyName("comparison")]
        public Dictionary<string, JsonElement> Comparison { get; set; } = new();
        
        [JsonPropertyName("best_scenario")]
        public string BestScenario { get; set; } = string.Empty;
        
        [JsonPropertyName("recommendations")]
        public List<string> Recommendations { get; set; } = new();
    }

    private class AiScenarioResult
    {
        [JsonPropertyName("timeline")]
        public List<AiMonthlySnapshot> Timeline { get; set; } = new();
        
        [JsonPropertyName("final_balance")]
        public double FinalBalance { get; set; }
        
        [JsonPropertyName("final_debt")]
        public double FinalDebt { get; set; }
        
        [JsonPropertyName("total_saved")]
        public double TotalSaved { get; set; }
        
        [JsonPropertyName("total_interest_paid")]
        public double TotalInterestPaid { get; set; }
        
        [JsonPropertyName("debt_paid_off")]
        public bool DebtPaidOff { get; set; }
        
        [JsonPropertyName("months_to_positive")]
        public int MonthsToPositive { get; set; }
    }

    private class AiMonthlySnapshot
    {
        [JsonPropertyName("month")]
        public int Month { get; set; }
        
        [JsonPropertyName("balance")]
        public double Balance { get; set; }
        
        [JsonPropertyName("debt")]
        public double Debt { get; set; }
        
        [JsonPropertyName("net_income")]
        public double NetIncome { get; set; }
    }

    private class AiScenarioScore
    {
        [JsonPropertyName("final_balance")]
        public double FinalBalance { get; set; }
        
        [JsonPropertyName("final_debt")]
        public double FinalDebt { get; set; }
        
        [JsonPropertyName("score")]
        public double Score { get; set; }
        
        [JsonPropertyName("debt_paid_off")]
        public bool DebtPaidOff { get; set; }
    }

    private class AiRiskAnalysisResponse
    {
        public int RiskScore { get; set; }
        public string RiskLevel { get; set; } = string.Empty;
        public List<string> Factors { get; set; } = new();
        public List<string> Recommendations { get; set; } = new();
        public AiRiskMetrics Metrics { get; set; } = new();
    }

    private class AiRiskMetrics
    {
        public double ExpenseRatio { get; set; }
        public double Volatility { get; set; }
        public double Balance { get; set; }
    }
}
