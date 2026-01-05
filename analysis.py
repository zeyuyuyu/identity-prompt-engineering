"""
实验结果分析脚本
定量分析 + 定性分析
"""

import json
import os
from collections import defaultdict
from typing import Dict, List
import statistics

def load_results(file_path: str = "results.json") -> List[Dict]:
    """加载实验结果"""
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def quantitative_analysis(results: List[Dict]) -> Dict:
    """
    定量分析
    """
    analysis = {
        "summary": {},
        "by_identity": defaultdict(lambda: {"responses": [], "latencies": [], "tokens": []}),
        "by_category": defaultdict(lambda: {"responses": [], "latencies": [], "tokens": []}),
        "by_identity_category": defaultdict(lambda: defaultdict(list)),
        "response_lengths": defaultdict(list)
    }
    
    successful_results = [r for r in results if r.get("success", False)]
    
    # 基础统计
    analysis["summary"]["total_experiments"] = len(results)
    analysis["summary"]["successful"] = len(successful_results)
    analysis["summary"]["failed"] = len(results) - len(successful_results)
    analysis["summary"]["success_rate"] = len(successful_results) / len(results) if results else 0
    
    for result in successful_results:
        identity = result["identity_name"]
        category = result["category"]
        response = result.get("response", "")
        latency = result.get("latency", 0)
        tokens = result.get("usage", {}).get("total_tokens", 0)
        
        # 按身份统计
        analysis["by_identity"][identity]["responses"].append(response)
        analysis["by_identity"][identity]["latencies"].append(latency)
        analysis["by_identity"][identity]["tokens"].append(tokens)
        
        # 按类别统计
        analysis["by_category"][category]["responses"].append(response)
        analysis["by_category"][category]["latencies"].append(latency)
        analysis["by_category"][category]["tokens"].append(tokens)
        
        # 响应长度
        analysis["response_lengths"][identity].append(len(response))
        
        # 身份x类别矩阵
        analysis["by_identity_category"][identity][category].append({
            "question_id": result["question_id"],
            "response_length": len(response),
            "tokens": tokens,
            "latency": latency
        })
    
    return analysis

def print_quantitative_report(analysis: Dict):
    """
    打印定量分析报告
    """
    print("\n" + "=" * 70)
    print("📊 定量分析报告")
    print("=" * 70)
    
    # 总体统计
    summary = analysis["summary"]
    print(f"\n📈 总体统计:")
    print(f"  总实验数: {summary['total_experiments']}")
    print(f"  成功: {summary['successful']} ({summary['success_rate']*100:.1f}%)")
    print(f"  失败: {summary['failed']}")
    
    # 按身份统计
    print(f"\n👤 按身份统计:")
    print("-" * 70)
    print(f"{'身份':<12} {'平均响应长度':<15} {'平均延迟(s)':<15} {'平均Token数':<15}")
    print("-" * 70)
    
    for identity, data in analysis["by_identity"].items():
        avg_length = statistics.mean([len(r) for r in data["responses"]]) if data["responses"] else 0
        avg_latency = statistics.mean(data["latencies"]) if data["latencies"] else 0
        avg_tokens = statistics.mean(data["tokens"]) if data["tokens"] else 0
        print(f"{identity:<12} {avg_length:<15.0f} {avg_latency:<15.2f} {avg_tokens:<15.0f}")
    
    # 按问题类别统计
    print(f"\n📁 按问题类别统计:")
    print("-" * 70)
    print(f"{'类别':<15} {'平均响应长度':<15} {'平均延迟(s)':<15} {'平均Token数':<15}")
    print("-" * 70)
    
    for category, data in analysis["by_category"].items():
        avg_length = statistics.mean([len(r) for r in data["responses"]]) if data["responses"] else 0
        avg_latency = statistics.mean(data["latencies"]) if data["latencies"] else 0
        avg_tokens = statistics.mean(data["tokens"]) if data["tokens"] else 0
        print(f"{category:<15} {avg_length:<15.0f} {avg_latency:<15.2f} {avg_tokens:<15.0f}")

def qualitative_analysis(results: List[Dict], output_file: str = "qualitative_report.md"):
    """
    定性分析 - 生成详细的对比报告
    """
    # 按问题ID分组
    by_question = defaultdict(list)
    for r in results:
        if r.get("success"):
            by_question[r["question_id"]].append(r)
    
    report_lines = [
        "# Identity Prompt Engineering 定性分析报告\n",
        f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "---\n\n"
    ]
    
    for question_id, responses in by_question.items():
        if not responses:
            continue
            
        question = responses[0]["question"]
        category = responses[0]["category"]
        
        report_lines.append(f"## 问题: {question_id}\n\n")
        report_lines.append(f"**类别:** {category}\n\n")
        report_lines.append(f"**问题内容:**\n> {question}\n\n")
        report_lines.append("---\n\n")
        
        for resp in responses:
            identity = resp["identity_name"]
            response_text = resp.get("response", "N/A")
            tokens = resp.get("usage", {}).get("total_tokens", "N/A")
            
            report_lines.append(f"### 身份: {identity}\n\n")
            report_lines.append(f"**Token数:** {tokens}\n\n")
            report_lines.append(f"**回答:**\n\n{response_text}\n\n")
            report_lines.append("---\n\n")
        
        report_lines.append("\n\n")
    
    # 保存报告
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(report_lines)
    
    print(f"\n📝 定性分析报告已保存到: {output_file}")
    return output_path

def compare_responses(results: List[Dict], question_id: str):
    """
    对比特定问题在不同身份下的回答
    """
    print(f"\n🔍 问题对比: {question_id}")
    print("=" * 70)
    
    question_results = [r for r in results if r["question_id"] == question_id and r.get("success")]
    
    if not question_results:
        print("未找到该问题的结果")
        return
    
    print(f"问题: {question_results[0]['question']}\n")
    
    for r in question_results:
        print(f"\n{'─' * 70}")
        print(f"👤 身份: {r['identity_name']}")
        print(f"📊 Token: {r.get('usage', {}).get('total_tokens', 'N/A')}")
        print(f"{'─' * 70}")
        response = r.get("response", "N/A")
        # 显示前500字符
        if len(response) > 500:
            print(f"{response[:500]}...\n[截断，共{len(response)}字符]")
        else:
            print(response)

def find_interesting_differences(results: List[Dict]) -> List[Dict]:
    """
    找出有趣的差异 - 同一问题下响应差异最大的情况
    """
    by_question = defaultdict(list)
    for r in results:
        if r.get("success"):
            by_question[r["question_id"]].append(r)
    
    differences = []
    
    for question_id, responses in by_question.items():
        if len(responses) < 2:
            continue
        
        lengths = [len(r.get("response", "")) for r in responses]
        length_variance = statistics.variance(lengths) if len(lengths) > 1 else 0
        
        differences.append({
            "question_id": question_id,
            "question": responses[0]["question"],
            "category": responses[0]["category"],
            "variance": length_variance,
            "min_length": min(lengths),
            "max_length": max(lengths),
            "num_responses": len(responses)
        })
    
    # 按差异排序
    differences.sort(key=lambda x: x["variance"], reverse=True)
    
    return differences

def print_interesting_differences(results: List[Dict], top_n: int = 5):
    """
    打印最有趣的差异
    """
    differences = find_interesting_differences(results)
    
    print(f"\n🔥 响应差异最大的 Top {top_n} 问题:")
    print("=" * 70)
    
    for i, diff in enumerate(differences[:top_n], 1):
        print(f"\n{i}. {diff['question_id']} (类别: {diff['category']})")
        print(f"   问题: {diff['question'][:60]}...")
        print(f"   响应长度范围: {diff['min_length']} - {diff['max_length']} 字符")
        print(f"   差异度: {diff['variance']:.0f}")

def generate_full_report(results_file: str = "results.json"):
    """
    生成完整分析报告
    """
    results = load_results(results_file)
    
    print("\n" + "🔬 " * 20)
    print("       Identity Prompt Engineering 实验分析")
    print("🔬 " * 20)
    
    # 定量分析
    analysis = quantitative_analysis(results)
    print_quantitative_report(analysis)
    
    # 有趣差异
    print_interesting_differences(results)
    
    # 生成定性报告
    qualitative_analysis(results)
    
    print("\n" + "=" * 70)
    print("✅ 分析完成！")
    print("=" * 70)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        results_file = sys.argv[1]
    else:
        # 默认尝试加载 demo 结果或完整结果
        if os.path.exists(os.path.join(os.path.dirname(__file__), "demo_results.json")):
            results_file = "demo_results.json"
        else:
            results_file = "results.json"
    
    generate_full_report(results_file)

