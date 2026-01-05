"""
Identity Prompt Engineering 实验主脚本
探索 System Prompt 中身份变化对 LLM 输出的影响
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from openai import OpenAI
from config import IDENTITIES, TEST_QUESTIONS, EXPERIMENT_PARAMS, OPENAI_MODEL

# 初始化 OpenAI 客户端
client = OpenAI()

def get_response(
    identity_key: str,
    question: str,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> Dict:
    """
    使用指定身份获取 LLM 响应
    """
    identity = IDENTITIES[identity_key]
    system_prompt = identity["system_prompt"]
    
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        end_time = time.time()
        
        return {
            "success": True,
            "response": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "latency": end_time - start_time
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": None
        }

def run_single_experiment(
    identity_key: str,
    question_data: Dict,
    run_id: int = 1
) -> Dict:
    """
    运行单次实验
    """
    result = get_response(
        identity_key=identity_key,
        question=question_data["question"],
        temperature=EXPERIMENT_PARAMS["temperature"],
        max_tokens=EXPERIMENT_PARAMS["max_tokens"]
    )
    
    return {
        "identity_key": identity_key,
        "identity_name": IDENTITIES[identity_key]["name"],
        "question_id": question_data["id"],
        "question": question_data["question"],
        "category": question_data["category"],
        "difficulty": question_data["difficulty"],
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        **result
    }

def run_full_experiment(
    identities: List[str] = None,
    categories: List[str] = None,
    num_runs: int = 1,
    output_file: str = "results.json"
) -> List[Dict]:
    """
    运行完整实验
    
    Args:
        identities: 要测试的身份列表，None 表示全部
        categories: 要测试的问题类别，None 表示全部
        num_runs: 每个组合运行次数
        output_file: 结果输出文件
    """
    if identities is None:
        identities = list(IDENTITIES.keys())
    
    if categories is None:
        categories = list(TEST_QUESTIONS.keys())
    
    results = []
    total_combinations = 0
    
    # 计算总组合数
    for category in categories:
        total_combinations += len(TEST_QUESTIONS[category]) * len(identities) * num_runs
    
    print(f"=" * 60)
    print(f"Identity Prompt Engineering 实验")
    print(f"=" * 60)
    print(f"模型: {OPENAI_MODEL}")
    print(f"身份数量: {len(identities)}")
    print(f"问题类别: {categories}")
    print(f"每组合运行次数: {num_runs}")
    print(f"总实验数: {total_combinations}")
    print(f"=" * 60)
    
    current = 0
    
    for category in categories:
        print(f"\n📁 类别: {category}")
        
        for question_data in TEST_QUESTIONS[category]:
            print(f"\n  ❓ 问题: {question_data['id']}")
            
            for identity_key in identities:
                identity_name = IDENTITIES[identity_key]["name"]
                
                for run in range(1, num_runs + 1):
                    current += 1
                    print(f"    [{current}/{total_combinations}] 身份: {identity_name}, 运行 #{run}...", end=" ")
                    
                    result = run_single_experiment(
                        identity_key=identity_key,
                        question_data=question_data,
                        run_id=run
                    )
                    results.append(result)
                    
                    if result["success"]:
                        print(f"✓ ({result['latency']:.2f}s, {result['usage']['total_tokens']} tokens)")
                    else:
                        print(f"✗ Error: {result.get('error', 'Unknown')}")
                    
                    # 避免 rate limiting
                    time.sleep(0.5)
    
    # 保存结果
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"✅ 实验完成！结果已保存到: {output_file}")
    print(f"成功: {sum(1 for r in results if r['success'])}/{len(results)}")
    print(f"{'=' * 60}")
    
    return results

def run_quick_demo():
    """
    快速演示：用少量身份和问题测试
    """
    print("\n🚀 快速演示模式")
    print("选择 3 个身份和 2 个问题进行测试\n")
    
    demo_identities = ["none", "doctor", "lawyer"]
    demo_categories = ["medical", "legal"]
    
    return run_full_experiment(
        identities=demo_identities,
        categories=demo_categories,
        num_runs=1,
        output_file="demo_results.json"
    )

def run_specific_test(identity_key: str, question: str):
    """
    单独测试特定身份和问题
    """
    print(f"\n🔬 单独测试")
    print(f"身份: {IDENTITIES[identity_key]['name']}")
    print(f"问题: {question[:50]}...")
    print("-" * 40)
    
    result = get_response(identity_key, question)
    
    if result["success"]:
        print(f"\n📝 回答:\n{result['response']}")
        print(f"\n📊 统计: {result['usage']['total_tokens']} tokens, {result['latency']:.2f}s")
    else:
        print(f"❌ 错误: {result['error']}")
    
    return result

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Identity Prompt Engineering 实验")
    parser.add_argument("--mode", choices=["demo", "full", "test"], default="demo",
                       help="运行模式: demo(快速演示), full(完整实验), test(单独测试)")
    parser.add_argument("--identity", type=str, help="测试特定身份 (test模式)")
    parser.add_argument("--question", type=str, help="测试特定问题 (test模式)")
    parser.add_argument("--runs", type=int, default=1, help="每组合运行次数")
    
    args = parser.parse_args()
    
    if args.mode == "demo":
        run_quick_demo()
    elif args.mode == "full":
        run_full_experiment(num_runs=args.runs)
    elif args.mode == "test":
        if args.identity and args.question:
            run_specific_test(args.identity, args.question)
        else:
            print("test 模式需要 --identity 和 --question 参数")
            print(f"可用身份: {list(IDENTITIES.keys())}")

