# Section E: Evaluation Methods

## Q37: Evaluation Metrics for Language Models

**Answer:**
Common evaluation metrics for language models include BLEU, ROUGE, METEOR, and perplexity.

**Implementation Examples:**

1. **BLEU Score Calculation:**
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu(reference, candidate):
    """
    Calculate BLEU score for a single sentence
    """
    smoothie = SmoothingFunction().method1
    return sentence_bleu(
        [reference.split()],
        candidate.split(),
        smoothing_function=smoothie
    )

# Usage example
reference = "the cat sits on the mat"
candidate = "the cat is sitting on the mat"
bleu_score = calculate_bleu(reference, candidate)
```

2. **ROUGE Score Calculation:**
```python
from rouge_score import rouge_scorer

def calculate_rouge(reference, candidate):
    """
    Calculate ROUGE scores
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
    scores = scorer.score(reference, candidate)
    return scores

# Usage example
reference = "the quick brown fox jumps over the lazy dog"
candidate = "the fast brown fox leaps over the lazy dog"
rouge_scores = calculate_rouge(reference, candidate)
```

3. **Perplexity Calculation:**
```python
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def calculate_perplexity(text):
    """
    Calculate perplexity using GPT-2
    """
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs['input_ids'])
        
    return torch.exp(outputs.loss).item()

# Usage example
text = "This is a sample sentence for perplexity calculation."
perplexity = calculate_perplexity(text)
```

## Q38: Human Evaluation Methods

**Answer:**
Human evaluation methods for assessing model outputs:

```python
class HumanEvaluation:
    def __init__(self):
        self.criteria = {
            'fluency': (1, 5),      # Scale 1-5
            'relevance': (1, 5),    # Scale 1-5
            'coherence': (1, 5),    # Scale 1-5
            'factuality': (0, 1)    # Binary score
        }
    
    def create_evaluation_form(self, response):
        """
        Generate evaluation form for human annotators
        """
        form = {
            'response': response,
            'scores': {
                criterion: None for criterion in self.criteria
            },
            'comments': ''
        }
        return form
    
    def calculate_metrics(self, evaluations):
        """
        Calculate aggregate metrics from multiple evaluations
        """
        metrics = {}
        for criterion in self.criteria:
            scores = [eval['scores'][criterion] for eval in evaluations]
            metrics[criterion] = {
                'mean': np.mean(scores),
                'std': np.std(scores),
                'median': np.median(scores)
            }
        return metrics

# Usage example
def run_human_evaluation(responses):
    evaluator = HumanEvaluation()
    evaluations = []
    
    for response in responses:
        form = evaluator.create_evaluation_form(response)
        # Collect human annotations (mock example)
        form['scores'] = {
            'fluency': 4,
            'relevance': 5,
            'coherence': 4,
            'factuality': 1
        }
        form['comments'] = "Clear and well-structured response"
        evaluations.append(form)
    
    return evaluator.calculate_metrics(evaluations)
```

## Q39: A/B Testing for Model Comparison

**Answer:**
Implementation of A/B testing for comparing different model versions:

```python
import scipy.stats as stats
import numpy as np

class ABTesting:
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level
    
    def calculate_sample_size(self, effect_size, power=0.8):
        """
        Calculate required sample size for the test
        """
        from statsmodels.stats.power import TTestIndPower
        analysis = TTestIndPower()
        sample_size = analysis.solve_power(
            effect_size=effect_size,
            power=power,
            alpha=1-self.confidence_level
        )
        return int(np.ceil(sample_size))
    
    def run_test(self, model_a_results, model_b_results):
        """
        Run statistical test to compare models
        """
        t_stat, p_value = stats.ttest_ind(
            model_a_results,
            model_b_results
        )
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(
            (np.var(model_a_results) + np.var(model_b_results)) / 2
        )
        effect_size = (
            np.mean(model_b_results) - np.mean(model_a_results)
        ) / pooled_std
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'effect_size': effect_size,
            'significant': p_value < (1 - self.confidence_level)
        }

# Usage example
def compare_models(model_a_responses, model_b_responses):
    ab_test = ABTesting()
    
    # Calculate required sample size
    sample_size = ab_test.calculate_sample_size(effect_size=0.5)
    
    # Run A/B test
    results = ab_test.run_test(
        model_a_responses,
        model_b_responses
    )
    return results
```

## Q40: Automated Evaluation Pipeline

**Answer:**
Implementation of an automated evaluation pipeline for model assessment:

```python
class EvaluationPipeline:
    def __init__(self):
        self.metrics = {
            'bleu': calculate_bleu,
            'rouge': calculate_rouge,
            'perplexity': calculate_perplexity
        }
    
    def evaluate_response(self, response, reference):
        """
        Evaluate a single response using multiple metrics
        """
        results = {}
        for metric_name, metric_fn in self.metrics.items():
            try:
                results[metric_name] = metric_fn(reference, response)
            except Exception as e:
                results[metric_name] = f"Error: {str(e)}"
        return results
    
    def evaluate_batch(self, responses, references):
        """
        Evaluate a batch of responses
        """
        results = []
        for response, reference in zip(responses, references):
            result = self.evaluate_response(response, reference)
            results.append(result)
        return results
    
    def generate_report(self, results):
        """
        Generate evaluation report
        """
        report = {
            'summary': {},
            'detailed_results': results
        }
        
        # Calculate summary statistics
        for metric in self.metrics.keys():
            metric_scores = [
                r[metric] for r in results
                if not isinstance(r[metric], str)
            ]
            if metric_scores:
                report['summary'][metric] = {
                    'mean': np.mean(metric_scores),
                    'std': np.std(metric_scores),
                    'min': np.min(metric_scores),
                    'max': np.max(metric_scores)
                }
        
        return report

# Usage example
def run_evaluation():
    pipeline = EvaluationPipeline()
    
    # Sample data
    responses = [
        "The model generated this response",
        "Another generated response"
    ]
    references = [
        "The expected response",
        "The reference response"
    ]
    
    # Run evaluation
    results = pipeline.evaluate_batch(responses, references)
    report = pipeline.generate_report(results)
    
    return report
```

## Q41: Error Analysis and Model Debugging

**Answer:**
Implementation of error analysis tools for model debugging:

```python
class ErrorAnalyzer:
    def __init__(self):
        self.error_categories = {
            'factual_error': self.check_factual_accuracy,
            'grammar_error': self.check_grammar,
            'coherence_error': self.check_coherence
        }
    
    def check_factual_accuracy(self, response, reference):
        """
        Check for factual errors using similarity metrics
        """
        similarity = calculate_semantic_similarity(response, reference)
        return similarity < 0.8
    
    def check_grammar(self, response):
        """
        Check for grammatical errors using language tool
        """
        import language_tool_python
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(response)
        return len(matches) > 0
    
    def check_coherence(self, response):
        """
        Check for coherence using sentence embeddings
        """
        sentences = response.split('.')
        if len(sentences) < 2:
            return False
        
        embeddings = generate_sentence_embeddings(sentences)
        coherence_scores = calculate_sentence_similarities(embeddings)
        return np.mean(coherence_scores) < 0.5
    
    def analyze_errors(self, response, reference):
        """
        Perform comprehensive error analysis
        """
        errors = {}
        for category, check_fn in self.error_categories.items():
            if category == 'factual_error':
                errors[category] = check_fn(response, reference)
            else:
                errors[category] = check_fn(response)
        
        return {
            'has_errors': any(errors.values()),
            'error_types': [k for k, v in errors.items() if v],
            'detailed_analysis': errors
        }

# Usage example
def debug_model_output(response, reference):
    analyzer = ErrorAnalyzer()
    analysis = analyzer.analyze_errors(response, reference)
    
    if analysis['has_errors']:
        print("Errors detected:")
        for error_type in analysis['error_types']:
            print(f"- {error_type}")
    
    return analysis
```

[End of Evaluation Methods Section] 