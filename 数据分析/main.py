# 导入必要依赖
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import matplotlib.pyplot as plt
import os
from tempfile import NamedTemporaryFile  # 用于创建临时文件，避免文件残留

# 初始化FastAPI应用
app = FastAPI(title="招聘数据统计接口")


@app.post("/analyze/salary_by_district", summary="按地区统计薪资并返回Excel")
async def analyze_salary_by_district(file: UploadFile = File(...)):
    """
    接收前端上传的招聘数据CSV，按地区统计薪资并返回Excel结果：
    - 步骤1：验证文件类型为CSV
    - 步骤2：读取CSV并检查必要字段
    - 步骤3：按地区分组计算薪资均值、最小值、最大值
    - 步骤4：将结果写入临时Excel并返回
    """
    # 验证文件类型
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="请上传CSV格式的文件")

    try:
        # 读取CSV文件（将文件流转换为DataFrame）
        df = pd.read_csv(file.file)

        # 检查必要字段是否存在
        required_columns = ["district", "salary"]
        if not set(required_columns).issubset(df.columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise HTTPException(status_code=400, detail=f"CSV缺少必要字段：{missing}")

        # 按地区分组统计薪资
        salary_stats = df.groupby("district")["salary"].agg(
            平均薪资="mean",
            最低薪资="min",
            最高薪资="max"
        ).reset_index()  # 将district从索引转为普通列

        # 创建临时Excel文件（避免占用本地磁盘，自动清理）
        with NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_excel:
            # 写入Excel（指定engine为openpyxl，支持xlsx格式）
            salary_stats.to_excel(temp_excel.name, index=False, engine="openpyxl")
            temp_path = temp_excel.name

        # 返回Excel文件给前端（下载时显示的文件名为"各地区薪资统计.xlsx"）
        return FileResponse(
            path=temp_path,
            filename="各地区薪资统计.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            background=lambda: os.unlink(temp_path)  # 下载完成后删除临时文件
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败：{str(e)}")


@app.post("/analyze/company_count_chart", summary="按地区统计公司数量并返回柱状图")
async def analyze_company_count_chart(file: UploadFile = File(..., description="包含district和companyId字段的CSV文件")):
    """
    接收前端上传的招聘数据CSV，按地区统计公司数量并返回柱状图PNG：
    - 步骤1：验证文件类型为CSV
    - 步骤2：读取CSV并检查必要字段
    - 步骤3：按地区统计不重复的公司数量
    - 步骤4：绘制柱状图并保存为临时PNG
    - 步骤5：返回图片文件给前端
    """
    # 验证文件类型
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="请上传CSV格式的文件")

    try:
        # 读取CSV文件
        df = pd.read_csv(file.file)

        # 检查必要字段是否存在
        required_columns = ["district", "companyId"]
        if not set(required_columns).issubset(df.columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise HTTPException(status_code=400, detail=f"CSV缺少必要字段：{missing}")

        # 按地区统计公司数量（去重，避免同一公司多次计数）
        company_count = df.groupby("district")["companyId"].nunique().reset_index(name="公司数量")

        # 绘制柱状图
        plt.figure(figsize=(10, 6))  # 设置画布大小
        plt.bar(
            x=company_count["district"],  # x轴：地区
            height=company_count["公司数量"],  # y轴：公司数量
            color="#4CAF50"  # 柱子颜色
        )
        plt.title("各地区招聘公司数量分布", fontsize=14)  # 标题
        plt.xlabel("地区", fontsize=12)  # x轴标签
        plt.ylabel("公司数量", fontsize=12)  # y轴标签
        plt.xticks(rotation=45, ha="right")  # x轴标签旋转45度，右对齐（避免重叠）
        plt.tight_layout()  # 自动调整布局，防止标签被截断

        # 创建临时图片文件
        with NamedTemporaryFile(suffix=".png", delete=False) as temp_png:
            plt.savefig(temp_png.name, dpi=150)  # 保存图片（dpi控制清晰度）
            temp_path = temp_png.name
        plt.close()  # 关闭画布，释放内存

        # 返回图片文件给前端
        return FileResponse(
            path=temp_path,
            filename="各地区公司数量分布.png",
            media_type="image/png",
            background=lambda: os.unlink(temp_path)  # 下载完成后删除临时文件
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败：{str(e)}")


