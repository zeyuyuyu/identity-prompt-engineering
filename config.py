"""
实验配置文件
Identity Prompt Engineering 实验
"""

# OpenAI 配置
OPENAI_MODEL = "gpt-4o"  # 或使用 "gpt-4-turbo", "gpt-4o-mini" 等可用模型

# 身份定义
IDENTITIES = {
    "none": {
        "name": "无身份",
        "system_prompt": "You are a helpful assistant."
    },
    "doctor": {
        "name": "医生",
        "system_prompt": "You are an experienced medical doctor with 20 years of clinical experience. You have expertise in internal medicine, diagnostics, and patient care. You approach problems with medical reasoning and evidence-based thinking."
    },
    "lawyer": {
        "name": "律师",
        "system_prompt": "You are a senior lawyer with 20 years of legal experience. You have expertise in contract law, civil litigation, and legal analysis. You approach problems with logical reasoning, attention to detail, and consideration of precedents."
    },
    "engineer": {
        "name": "工程师",
        "system_prompt": "You are a senior software engineer with 20 years of experience. You have expertise in system design, algorithms, and problem-solving. You approach problems systematically with technical precision."
    },
    "teacher": {
        "name": "教师",
        "system_prompt": "You are an experienced educator with 20 years of teaching experience. You have expertise in pedagogy, curriculum design, and student engagement. You approach problems by breaking them down into understandable components."
    },
    "scientist": {
        "name": "科学家",
        "system_prompt": "You are a research scientist with 20 years of experience. You have expertise in experimental design, data analysis, and scientific methodology. You approach problems with hypothesis-driven thinking and empirical reasoning."
    },
    "philosopher": {
        "name": "哲学家",
        "system_prompt": "You are a philosopher with 20 years of academic experience. You have expertise in logic, ethics, and critical thinking. You approach problems by examining underlying assumptions and exploring multiple perspectives."
    },
    "businessman": {
        "name": "商人",
        "system_prompt": "You are a successful business executive with 20 years of experience. You have expertise in strategy, negotiation, and market analysis. You approach problems with a focus on practical outcomes and value creation."
    }
}

# 测试问题集 - 分为多个类别
TEST_QUESTIONS = {
    # 医学相关问题
    "medical": [
        {
            "id": "med_1",
            "question": "我最近经常头痛，尤其是下午的时候，伴随着眼睛疲劳。这可能是什么原因？我应该怎么办？",
            "category": "medical",
            "difficulty": "easy"
        },
        {
            "id": "med_2", 
            "question": "如果一个人同时服用阿司匹林和华法林，可能会有什么风险？为什么？",
            "category": "medical",
            "difficulty": "hard"
        }
    ],
    
    # 法律相关问题
    "legal": [
        {
            "id": "legal_1",
            "question": "我的邻居在未经我同意的情况下，把他的围栏建到了我的土地上。我应该怎么处理这种情况？",
            "category": "legal",
            "difficulty": "easy"
        },
        {
            "id": "legal_2",
            "question": "在合同中，'不可抗力条款'和'情势变更原则'有什么区别？在什么情况下可以援引它们？",
            "category": "legal",
            "difficulty": "hard"
        }
    ],
    
    # 逻辑推理问题
    "logic": [
        {
            "id": "logic_1",
            "question": "有5个人参加比赛：A、B、C、D、E。已知：A比B快，C比D慢，E不是第一也不是最后，B比E慢，D比A快。请问谁是第一名？",
            "category": "logic",
            "difficulty": "medium"
        },
        {
            "id": "logic_2",
            "question": "一个岛上有100个人，其中有些人眼睛是蓝色的，有些人眼睛是棕色的。岛上有个规则：如果有人知道自己眼睛是蓝色的，他必须在当天午夜离开。岛上没有镜子，人们不能讨论眼睛颜色。一天，一个外来者说'这个岛上至少有一个人有蓝眼睛'。如果岛上恰好有3个人有蓝眼睛，会发生什么？",
            "category": "logic",
            "difficulty": "hard"
        }
    ],
    
    # 伦理道德问题
    "ethics": [
        {
            "id": "ethics_1",
            "question": "电车难题：一辆失控的电车正驶向5个被绑在轨道上的人。你可以拉一个开关，让电车转向另一条轨道，但那条轨道上有1个人。你会怎么做？请详细解释你的推理过程。",
            "category": "ethics",
            "difficulty": "medium"
        },
        {
            "id": "ethics_2",
            "question": "一家公司发现其产品有轻微缺陷，有0.01%的概率造成伤害。召回产品会导致公司破产，数千员工失业。如果不召回，统计上可能会有几个人受伤。作为CEO，你会怎么决定？",
            "category": "ethics",
            "difficulty": "hard"
        }
    ],
    
    # 创意问题
    "creative": [
        {
            "id": "creative_1",
            "question": "请用一个比喻来解释量子纠缠现象，让一个12岁的孩子能够理解。",
            "category": "creative",
            "difficulty": "medium"
        },
        {
            "id": "creative_2",
            "question": "如果你可以和历史上任何一个人共进晚餐，你会选择谁？你会问他们什么问题？请从你的专业角度来回答。",
            "category": "creative",
            "difficulty": "easy"
        }
    ],
    
    # 挑战性问题（LLM通常难以回答）
    "challenging": [
        {
            "id": "challenge_1",
            "question": "请解释为什么'这句话是假的'这个悖论会产生矛盾，并提出一个可能的解决方案。",
            "category": "challenging",
            "difficulty": "hard"
        },
        {
            "id": "challenge_2",
            "question": "如何证明你不是在一个模拟世界中？或者说，这个问题是否有意义？",
            "category": "challenging",
            "difficulty": "hard"
        }
    ]
}

# 评估维度
EVALUATION_DIMENSIONS = [
    "accuracy",       # 准确性 (1-5)
    "depth",          # 深度 (1-5)
    "relevance",      # 相关性 (1-5)
    "confidence",     # 置信度 (1-5)
    "professionalism" # 专业性 (1-5)
]

# 实验参数
EXPERIMENT_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "num_runs": 3,  # 每个组合运行次数，用于稳定性分析
}

