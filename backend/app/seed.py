"""初始化演示数据。仅在库为空时执行。"""
from datetime import date, timedelta

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.company import CmpCompany, CmpReview, CmpSalary
from app.models.job import JobApplication, JobPosition
from app.models.plan import PlnDailyTask, PlnLearningPath, PlnPlan
from app.models.prepare import PrpOffer, PrpQuestionBank
from app.models.rental import RntListing
from app.models.resume import RsmResume, RsmSection
from app.models.system import SysUserQuota
from app.models.user import UsrUser

DEMO_EMAIL = "demo@leappath.app"
DEMO_PASSWORD = "leappath"


def seed_if_empty():
    db = SessionLocal()
    try:
        if db.query(UsrUser).filter(UsrUser.email == DEMO_EMAIL).first():
            return
        _seed(db)
    finally:
        db.close()


def _seed(db):
    # ---------- 用户 ----------
    user = UsrUser(
        email=DEMO_EMAIL,
        password_hash=hash_password(DEMO_PASSWORD),
        nickname="李跃",
        gender=1,
        birth_year=1998,
        current_city="深圳",
        target_cities=["深圳", "广州", "杭州"],
        education_level="本科",
        years_of_experience=3,
        current_industry="互联网",
        target_industries=["互联网", "金融科技"],
        target_positions=["后端开发工程师", "Java 高级工程师"],
        expected_salary_min=25000,
        expected_salary_max=40000,
    )
    db.add(user)
    db.flush()
    db.add(SysUserQuota(user_id=user.id, interview_quota_total=10, interview_quota_used=2,
                        quota_reset_date=date.today() + timedelta(days=20)))

    # ---------- 简历 ----------
    resume = RsmResume(user_id=user.id, title="后端开发-主简历", is_default=True,
                       template_id="internet-modern", status="complete", score_total=85)
    db.add(resume)
    db.flush()
    sections = [
        ("personal_info", 0, {"name": "李跃", "phone": "138****8888", "email": DEMO_EMAIL,
                               "city": "深圳", "intent": "后端开发工程师"}),
        ("education", 1, {"items": [{"school": "华南理工大学", "major": "计算机科学与技术",
                                       "degree": "本科", "start": "2016-09", "end": "2020-06"}]}),
        ("experience", 2, {"items": [{"company": "某互联网公司", "role": "后端开发工程师",
                                        "start": "2020-07", "end": "至今",
                                        "desc": "负责公司后端 API 开发，提升了系统性能"}]}),
        ("project", 3, {"items": [{"name": "高并发订单系统", "role": "核心开发",
                                     "desc": "参与订单系统的重构，优化了数据库查询"}]}),
        ("skill", 4, {"tags": ["Java", "Spring Boot", "MySQL", "Redis", "Kafka", "Docker"]}),
        ("self_evaluation", 5, {"text": "扎实的后端基础，有较强的学习能力和团队协作精神。"}),
    ]
    for st, order, content in sections:
        db.add(RsmSection(resume_id=resume.id, section_type=st, sort_order=order, content=content))

    # ---------- 公司 ----------
    companies_data = [
        ("腾讯科技（深圳）有限公司", "腾讯", "互联网", "5000+", "listed", "深圳",
         "深圳市南山区科技中一路腾讯大厦", 113.9345, 22.5400, "high",
         ["C++", "Go", "微服务"], ["扁平化", "偶尔加班", "免费三餐"]),
        ("字节跳动", "字节", "互联网", "5000+", "listed", "深圳",
         "深圳市南山区深圳湾科技生态园", 113.9510, 22.5180, "extreme",
         ["Go", "Python", "大数据"], ["大小周", "扁平", "弹性工作"]),
        ("美团", "美团", "互联网", "5000+", "listed", "深圳",
         "深圳市福田区卓越世纪中心", 114.0588, 22.5430, "high",
         ["Java", "Spring", "分布式"], ["双休", "成长快", "餐补"]),
        ("招商银行", "招行", "金融科技", "5000+", "listed", "深圳",
         "深圳市福田区深南大道招银大厦", 114.0625, 22.5360, "medium",
         ["Java", "Oracle", "金融云"], ["稳定", "双休", "高公积金"]),
    ]
    companies = []
    for (name, short, ind, size, fin, city, addr, lng, lat, diff, tech, culture) in companies_data:
        c = CmpCompany(name=name, short_name=short, industry=ind, size_range=size,
                       financing_stage=fin, location_city=city, location_address=addr,
                       lng=lng, lat=lat, difficulty_level=diff, tech_stack=tech,
                       culture_tags=culture, data_source="seed",
                       description=f"{short}是国内领先的{ind}公司。")
        db.add(c)
        db.flush()
        companies.append(c)
        # 薪资
        for pos, lo, hi in [("后端开发", 25000, 50000), ("前端开发", 22000, 45000),
                            ("产品经理", 20000, 40000), ("算法工程师", 30000, 60000)]:
            db.add(CmpSalary(company_id=c.id, position_name=pos, salary_min=lo, salary_max=hi,
                             salary_avg=(lo + hi) // 2, bonus_months=4, sample_count=120,
                             data_year=2026, data_source="脉脉"))
        # 面经
        db.add(CmpReview(company_id=c.id, review_type="interview", position_name="后端开发",
                         interview_round="3轮", interview_difficulty=4,
                         interview_questions=["介绍一个有挑战的项目", "MySQL 索引原理",
                                               "如何设计一个秒杀系统", "Redis 持久化机制"],
                         review_content="一面问了算法题和项目经验，二面系统设计，三面 HR。整体偏难但公平。",
                         offer_result="offer", publish_date=date.today() - timedelta(days=20),
                         data_source="牛客"))

    # ---------- 职位 ----------
    positions = []
    job_data = [
        (companies[0], "后端开发工程师", "技术", 25000, 50000, "3-5年", "本科",
         "负责核心业务后端系统设计与开发，保障高并发场景下的稳定性。",
         "熟悉 Java/Go，掌握 Spring Boot、MySQL、Redis、Kafka，了解微服务与分布式。"),
        (companies[1], "Go 高级开发工程师", "基础架构", 30000, 55000, "3-5年", "本科",
         "参与基础架构与中台系统建设，承接超大规模流量。",
         "精通 Go，熟悉 Kubernetes、Docker，有大规模分布式系统经验优先。"),
        (companies[2], "Java 工程师", "交易平台", 24000, 42000, "1-3年", "本科",
         "负责交易平台后端开发，参与系统重构与性能优化。",
         "熟悉 Java、Spring、MySQL，了解 Redis、消息队列。"),
        (companies[3], "金融科技后端", "金融云", 22000, 38000, "1-3年", "本科",
         "负责金融云相关后端服务开发，保障数据安全与合规。",
         "熟悉 Java，了解金融业务，有较强的责任心与稳定性偏好。"),
    ]
    for (c, title, dept, lo, hi, exp, edu, desc, req) in job_data:
        p = JobPosition(company_id=c.id, title=title, department=dept, location_city=c.location_city,
                        salary_min=lo, salary_max=hi, salary_period="month", experience_required=exp,
                        education_required=edu, job_description=desc, job_requirements=req,
                        job_tags=["五险一金", "弹性工作", "扁平管理"], job_type="fulltime",
                        source_platform="seed", posted_date=date.today() - timedelta(days=5))
        db.add(p)
        db.flush()
        positions.append(p)

    # ---------- 投递 ----------
    app_data = [
        (positions[0], "腾讯科技（深圳）有限公司", "后端开发工程师", "interview", "25-50K", 6),
        (positions[1], "字节跳动", "Go 高级开发工程师", "applied", "30-55K", 3),
        (positions[2], "美团", "Java 工程师", "screening", "24-42K", 4),
        (positions[3], "招商银行", "金融科技后端", "saved", "22-38K", 0),
    ]
    for (p, cname, ptitle, status, salary, days_ago) in app_data:
        db.add(JobApplication(user_id=user.id, position_id=p.id, company_name=cname,
                              position_title=ptitle, status=status, salary_label=salary,
                              applied_date=date.today() - timedelta(days=days_ago) if status != "saved" else None,
                              status_history=[{"status": status, "at": str(date.today())}]))

    # ---------- 求职规划 ----------
    target = date.today() + timedelta(days=70)
    db.add(PlnPlan(user_id=user.id, target_industry="互联网", target_position="后端开发工程师",
                   target_start_date=target, current_progress=60,
                   timeline=[
                       {"phase": "准备期", "desc": "简历优化 · 技能提升 · 模拟面试", "weeks_before": 12},
                       {"phase": "投递期", "desc": "精准投递 · 跟进反馈", "weeks_before": 8},
                       {"phase": "密集面试期", "desc": "多轮面试 · 复盘提升", "weeks_before": 4},
                       {"phase": "Offer 谈判期", "desc": "薪资谈判 · Offer 对比", "weeks_before": 2},
                       {"phase": "入职", "desc": "背调 · 租房选址", "weeks_before": 0},
                   ]))
    for i, (ttype, title) in enumerate([
        ("apply", "投递 3 份简历"),
        ("interview", "完成 1 次模拟面试"),
        ("study", "学习系统设计 2 小时"),
    ]):
        db.add(PlnDailyTask(user_id=user.id, task_date=date.today(), task_type=ttype, title=title,
                            is_completed=(i == 2), sort_order=i))
    db.add(PlnLearningPath(user_id=user.id, skill_name="系统设计", estimated_hours=30, completed_hours=12,
                           resources=[{"type": "course", "title": "系统设计入门", "url": "#", "priority": "high"},
                                       {"type": "book", "title": "DDIA", "url": "#", "priority": "high"}]))

    # ---------- 题库 ----------
    questions = [
        ("technical", "后端", "medium", "请解释 MySQL 的索引原理及最左前缀匹配。",
         "B+ 树索引，叶子节点存数据，最左前缀指联合索引从左到右匹配。",
         ["B+树结构", "聚簇/非聚簇索引", "最左前缀"]),
        ("technical", "后端", "hard", "如何设计一个高并发秒杀系统？",
         "限流、缓存预热、库存原子扣减、异步下单、削峰填谷。",
         ["限流", "Redis 扣库存", "MQ 异步", "防超卖"]),
        ("technical", "前端", "medium", "说说浏览器从输入 URL 到页面展示的过程。",
         "DNS 解析 → TCP → HTTP → 渲染（解析 DOM/CSSOM → 布局 → 绘制）。",
         ["DNS", "TCP/HTTP", "渲染流程"]),
        ("technical", "算法", "easy", "如何判断一个链表是否有环？",
         "快慢指针，相遇则有环。",
         ["双指针", "Floyd 判环"]),
        ("common", "自我介绍", "easy", "请做一个 1 分钟的自我介绍。",
         "包含：身份定位 + 核心经历 + 匹配岗位的亮点 + 求职意向。",
         ["结构化", "突出匹配度"]),
        ("common", "职业规划", "easy", "你未来 3 年的职业规划是怎样的？",
         "短期夯实技术、中期承担更大职责、长期向技术专家/管理发展。",
         ["分阶段", "与岗位关联"]),
        ("aptitude", "逻辑推理", "medium", "数列 2, 6, 12, 20, 30, ? 下一项是多少？",
         "42。相邻差为 4,6,8,10,12，故下一项 30+12=42。",
         ["找规律", "等差递增"]),
    ]
    for (cat, sub, diff, q, a, tips) in questions:
        db.add(PrpQuestionBank(category=cat, sub_category=sub, difficulty=diff, question=q,
                               answer=a, answer_tips=tips, tags=[sub], source="seed"))

    # ---------- Offer ----------
    db.add(PrpOffer(user_id=user.id, company_name="腾讯", position_title="后端开发工程师",
                    base_salary=35000, bonus_months=6, stock_value=80000,
                    total_annual=35000 * 18 + 80000, work_city="深圳", commute_time=35,
                    evaluation={"salary": 4, "growth": 5, "wlb": 3, "location": 4, "stability": 4, "team": 5}))
    db.add(PrpOffer(user_id=user.id, company_name="招商银行", position_title="金融科技后端",
                    base_salary=28000, bonus_months=8, stock_value=0,
                    total_annual=28000 * 20, work_city="深圳", commute_time=25,
                    evaluation={"salary": 3, "growth": 3, "wlb": 5, "location": 5, "stability": 5, "team": 4}))

    # ---------- 房源（围绕公司坐标分布） ----------
    base_lng, base_lat = 113.9345, 22.5400  # 腾讯大厦附近
    rental_samples = [
        ("阳光花园 2室1厅 近地铁", "南山区", "阳光花园", 0.012, 0.008, 3200, "2room", "whole", 65, "中层", "南"),
        ("翠苑新村 1室1厅 精装", "南山区", "翠苑新村", -0.006, 0.004, 2500, "1room", "whole", 45, "高层", "东南"),
        ("碧海名园 3室1厅 拎包入住", "南山区", "碧海名园", 0.020, -0.010, 4500, "3room", "whole", 95, "低层", "南"),
        ("科技园合租主卧", "南山区", "科技园公寓", 0.004, 0.002, 1800, "studio", "share", 18, "中层", "西"),
        ("后海地铁口次卧", "南山区", "后海花园", -0.014, 0.012, 2100, "1room", "share", 22, "高层", "北"),
        ("白石洲温馨一居", "南山区", "白石洲", 0.030, 0.018, 2300, "1room", "whole", 38, "中层", "东"),
        ("蛇口海景两房", "南山区", "蛇口海湾", -0.025, -0.022, 5200, "2room", "whole", 78, "高层", "南"),
        ("西丽大学城单间", "南山区", "西丽公寓", 0.045, 0.035, 1600, "studio", "share", 16, "低层", "东南"),
    ]
    for (title, dist, comm, dlng, dlat, price, rtype, rent, area, floor, orient) in rental_samples:
        db.add(RntListing(title=title, city="深圳", district=dist, community_name=comm,
                          address=f"深圳市{dist}{comm}", lng=base_lng + dlng, lat=base_lat + dlat,
                          price_monthly=price, price_deposit="押一付三", room_type=rtype, rent_type=rent,
                          area_sqm=area, floor_level={"低层": "low", "中层": "mid", "高层": "high"}[floor],
                          orientation=orient, decoration="fine", has_elevator=True, has_balcony=True,
                          has_private_bath=(rent == "whole"),
                          facilities=["床", "空调", "洗衣机", "冰箱", "宽带"],
                          nearby_poi=[{"type": "subway", "name": "地铁站", "distance_m": 300}],
                          source_platform="seed", listed_date=date.today() - timedelta(days=3)))
    # 杭州少量房源用于城市对比
    for title, price in [("杭州西湖区一居", 3000), ("杭州滨江两居", 3800)]:
        db.add(RntListing(title=title, city="杭州", district="西湖区", community_name="示例小区",
                          lng=120.15, lat=30.27, price_monthly=price, room_type="1room",
                          rent_type="whole", area_sqm=50, source_platform="seed"))

    db.commit()
