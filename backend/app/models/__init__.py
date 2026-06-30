"""所有 ORM 模型（按模块拆分，表名带模块前缀）。"""
from .company import CmpCompany, CmpReview, CmpSalary, CmpUserSaved
from .interview import ItvMessage, ItvReport, ItvSession
from .job import JobApplication, JobPosition
from .plan import PlnDailyTask, PlnLearningPath, PlnPlan, PlnSkillAssessment
from .prepare import PrpOffer, PrpPracticeRecord, PrpQuestionBank
from .rental import RntCommute, RntListing
from .resume import RsmResume, RsmSection, RsmVersion
from .system import SysAiLog, SysUserQuota
from .user import UsrUser

__all__ = [
    "UsrUser",
    "RsmResume",
    "RsmSection",
    "RsmVersion",
    "JobPosition",
    "JobApplication",
    "CmpCompany",
    "CmpSalary",
    "CmpReview",
    "CmpUserSaved",
    "ItvSession",
    "ItvMessage",
    "ItvReport",
    "PlnPlan",
    "PlnSkillAssessment",
    "PlnLearningPath",
    "PlnDailyTask",
    "PrpQuestionBank",
    "PrpPracticeRecord",
    "PrpOffer",
    "RntListing",
    "RntCommute",
    "SysUserQuota",
    "SysAiLog",
]
