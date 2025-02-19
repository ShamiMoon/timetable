import pandas as pd
import re,os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def process_week(week_str: str):
    week_ranges = re.findall(r'\d+-\d+|\d+', week_str)
    expanded_weeks = []

    for week in week_ranges:
        if '-' in week:
            start, end = map(int, week.split('-'))
            expanded_weeks.extend(map(str, range(start, end + 1)))
        else:
            expanded_weeks.append(week)

    return ', '.join(expanded_weeks)

def get_today_week_and_day():
    start_date_str = "2025-02-24"
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    today = datetime.today()
    today_weekday = today.weekday()
    days_diff = (today - start_date).days
    current_week = days_diff // 7 + 1
    return today_weekday, current_week

def process_timetable():
    filePath = os.path.join(BASE_DIR, "data/timetable.xlsx")
    df = pd.read_excel(filePath)
    df.fillna(method='ffill', inplace=True)
    df["周次_origin"] = df["周次"]
    df['周次'] = df['周次'].apply(process_week)
    week_order = ['日', '一', '二', '三', '四', '五', '六']
    df['星期'] = pd.Categorical(df['星期'], categories=week_order, ordered=True)
    df_sorted = df.sort_values(by=['星期', '节次'])

    return df_sorted


def displayable_all_timetable():
    df = process_timetable()
    df_all = df[["星期",'节次', '课程名', '教师', '教室', "周次_origin"]]
    df_all.columns.values[5] = "周次"
    print(df_all.to_string(index=False))
    return df_all.to_string(index=False)

def filter_and_display_timetable(week_day: str, target_week: int):
    df = process_timetable()
    df_filtered = df[df['星期'] == week_day]
    df_filtered = df_filtered[df_filtered['周次'].str.contains(str(target_week))]
    df_filtered = df_filtered[['节次', '课程名', '教师', '教室']]
    if df_filtered.empty:
        return "你今天没有课哦!"
    return df_filtered.to_string(index=False)

def display_today_timetable():
    df = process_timetable()
    today_weekday, current_week = get_today_week_and_day()

    week_days = ['一', '二', '三', '四', '五', '六', '日']
    week_day_str = week_days[today_weekday]
    if current_week < 1:
        print(f"今天是星期{week_day_str}，当前在假期中")
        return "当前在假期中"
    print(f"今天是星期{week_day_str}，当前是第{current_week}周：")
    print(filter_and_display_timetable(df, week_day_str, current_week))
    return filter_and_display_timetable(df, week_day_str, current_week)

def display_thisWeek_timeable():
    df = process_timetable()
    today_weekday, current_week = get_today_week_and_day()
    df_filtered = df[df['周次'].str.contains(str(current_week))]
    df_filtered = df_filtered[["星期",'节次', '课程名', '教师', '教室']]
    if df_filtered.empty:
        print("你本周没有课哦!")
        return "你本周没有课哦!"
    print(df_filtered.to_string(index=False))
    return df_filtered.to_string(index=False)


if __name__ == "__main__":
    display_today_timetable()
    display_thisWeek_timeable()
    # print(filter_and_display_timetable(processed_df, "三", "11"))
    # print(displayable_all_timetable(processed_df))
