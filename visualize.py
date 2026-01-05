"""
实验结果可视化
生成图表展示不同身份对响应的影响
"""

import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

def load_results(file_path: str = "results.json"):
    """加载实验结果"""
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_response_length_by_identity(results, save_path: str = "viz_length_by_identity.png"):
    """
    图1: 不同身份的平均响应长度
    """
    # 按身份聚合
    by_identity = defaultdict(list)
    for r in results:
        if r.get("success") and r.get("response"):
            by_identity[r["identity_name"]].append(len(r["response"]))
    
    identities = list(by_identity.keys())
    avg_lengths = [np.mean(by_identity[i]) for i in identities]
    std_lengths = [np.std(by_identity[i]) for i in identities]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(identities, avg_lengths, yerr=std_lengths, capsize=5, 
                  color=plt.cm.Set3(np.linspace(0, 1, len(identities))))
    
    ax.set_xlabel('身份', fontsize=12)
    ax.set_ylabel('平均响应长度 (字符)', fontsize=12)
    ax.set_title('不同身份的平均响应长度对比', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    
    # 添加数值标签
    for bar, val in zip(bars, avg_lengths):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{val:.0f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    full_path = os.path.join(os.path.dirname(__file__), save_path)
    plt.savefig(full_path, dpi=150)
    plt.close()
    print(f"✅ 已保存: {save_path}")

def plot_token_usage_by_identity(results, save_path: str = "viz_tokens_by_identity.png"):
    """
    图2: 不同身份的Token使用量
    """
    by_identity = defaultdict(list)
    for r in results:
        if r.get("success"):
            tokens = r.get("usage", {}).get("total_tokens", 0)
            by_identity[r["identity_name"]].append(tokens)
    
    identities = list(by_identity.keys())
    avg_tokens = [np.mean(by_identity[i]) for i in identities]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(identities)))
    bars = ax.barh(identities, avg_tokens, color=colors)
    
    ax.set_xlabel('平均Token数', fontsize=12)
    ax.set_ylabel('身份', fontsize=12)
    ax.set_title('不同身份的Token使用量对比', fontsize=14, fontweight='bold')
    
    # 添加数值标签
    for bar, val in zip(bars, avg_tokens):
        ax.text(val + 10, bar.get_y() + bar.get_height()/2, 
                f'{val:.0f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    full_path = os.path.join(os.path.dirname(__file__), save_path)
    plt.savefig(full_path, dpi=150)
    plt.close()
    print(f"✅ 已保存: {save_path}")

def plot_heatmap_identity_category(results, save_path: str = "viz_heatmap.png"):
    """
    图3: 身份x类别 热力图 (响应长度)
    """
    # 构建矩阵
    data = defaultdict(lambda: defaultdict(list))
    for r in results:
        if r.get("success") and r.get("response"):
            data[r["identity_name"]][r["category"]].append(len(r["response"]))
    
    identities = sorted(set(r["identity_name"] for r in results if r.get("success")))
    categories = sorted(set(r["category"] for r in results if r.get("success")))
    
    matrix = np.zeros((len(identities), len(categories)))
    for i, identity in enumerate(identities):
        for j, category in enumerate(categories):
            if data[identity][category]:
                matrix[i, j] = np.mean(data[identity][category])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(np.arange(len(categories)))
    ax.set_yticks(np.arange(len(identities)))
    ax.set_xticklabels(categories)
    ax.set_yticklabels(identities)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # 添加数值
    for i in range(len(identities)):
        for j in range(len(categories)):
            text = ax.text(j, i, f'{matrix[i, j]:.0f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    ax.set_title('身份 × 问题类别 响应长度热力图', fontsize=14, fontweight='bold')
    fig.colorbar(im, ax=ax, label='平均响应长度')
    
    plt.tight_layout()
    full_path = os.path.join(os.path.dirname(__file__), save_path)
    plt.savefig(full_path, dpi=150)
    plt.close()
    print(f"✅ 已保存: {save_path}")

def plot_latency_comparison(results, save_path: str = "viz_latency.png"):
    """
    图4: 响应延迟对比
    """
    by_identity = defaultdict(list)
    for r in results:
        if r.get("success"):
            by_identity[r["identity_name"]].append(r.get("latency", 0))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    data = [by_identity[identity] for identity in by_identity.keys()]
    labels = list(by_identity.keys())
    
    bp = ax.boxplot(data, labels=labels, patch_artist=True)
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(labels)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_xlabel('身份', fontsize=12)
    ax.set_ylabel('响应延迟 (秒)', fontsize=12)
    ax.set_title('不同身份的响应延迟分布', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    full_path = os.path.join(os.path.dirname(__file__), save_path)
    plt.savefig(full_path, dpi=150)
    plt.close()
    print(f"✅ 已保存: {save_path}")

def plot_category_comparison(results, save_path: str = "viz_category_comparison.png"):
    """
    图5: 不同问题类别下身份效应对比
    """
    data = defaultdict(lambda: defaultdict(list))
    for r in results:
        if r.get("success") and r.get("response"):
            data[r["category"]][r["identity_name"]].append(len(r["response"]))
    
    categories = list(data.keys())
    if not categories:
        print("⚠️ 无数据可视化")
        return
        
    identities = list(set(
        identity 
        for category_data in data.values() 
        for identity in category_data.keys()
    ))
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, category in enumerate(categories[:6]):  # 最多6个类别
        ax = axes[idx]
        
        cat_identities = list(data[category].keys())
        avg_lengths = [np.mean(data[category][i]) if data[category][i] else 0 for i in cat_identities]
        
        bars = ax.bar(range(len(cat_identities)), avg_lengths, 
                     color=plt.cm.tab10(np.linspace(0, 1, len(cat_identities))))
        ax.set_xticks(range(len(cat_identities)))
        ax.set_xticklabels(cat_identities, rotation=45, ha='right', fontsize=8)
        ax.set_title(f'{category}', fontsize=11, fontweight='bold')
        ax.set_ylabel('响应长度')
    
    # 隐藏多余的子图
    for idx in range(len(categories), len(axes)):
        axes[idx].axis('off')
    
    fig.suptitle('不同问题类别下各身份的响应长度对比', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    full_path = os.path.join(os.path.dirname(__file__), save_path)
    plt.savefig(full_path, dpi=150)
    plt.close()
    print(f"✅ 已保存: {save_path}")

def generate_all_visualizations(results_file: str = "results.json"):
    """
    生成所有可视化图表
    """
    print("\n📊 生成可视化图表...")
    print("=" * 50)
    
    results = load_results(results_file)
    successful_results = [r for r in results if r.get("success")]
    
    if not successful_results:
        print("❌ 没有成功的实验结果可供可视化")
        return
    
    print(f"加载了 {len(successful_results)} 条成功结果")
    
    try:
        plot_response_length_by_identity(successful_results)
    except Exception as e:
        print(f"⚠️ 图1生成失败: {e}")
    
    try:
        plot_token_usage_by_identity(successful_results)
    except Exception as e:
        print(f"⚠️ 图2生成失败: {e}")
    
    try:
        plot_heatmap_identity_category(successful_results)
    except Exception as e:
        print(f"⚠️ 图3生成失败: {e}")
    
    try:
        plot_latency_comparison(successful_results)
    except Exception as e:
        print(f"⚠️ 图4生成失败: {e}")
    
    try:
        plot_category_comparison(successful_results)
    except Exception as e:
        print(f"⚠️ 图5生成失败: {e}")
    
    print("\n" + "=" * 50)
    print("✅ 可视化完成！")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        results_file = sys.argv[1]
    else:
        if os.path.exists(os.path.join(os.path.dirname(__file__), "demo_results.json")):
            results_file = "demo_results.json"
        else:
            results_file = "results.json"
    
    generate_all_visualizations(results_file)

