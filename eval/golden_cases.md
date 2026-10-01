# Golden cases (illustrative)

End-to-end test cases. Each row: input / expected intent / expected tool / must-refuse?

| Input | Intent | Expected tool | Must-refuse |
|---|---|---|---|
| 张三今天考勤怎么样？ | attendance | query_student_attendance(张三, today) | no |
| 帮我看看李四最近有没有迟到 | attendance | query_student_attendance(李四) | no |
| 今天有什么考勤预警？ | attendance | get_attendance_warning() | no |
| 明天第二节是什么课？ | schedule | get_course_schedule(?) | no |
| 帮我写一首关于秋天的诗 | off_topic | fallback | **yes** |
| 1+1等于几 | off_topic | fallback | **yes** |
| 你们公司股价多少 | off_topic | fallback | **yes** |

Production had 500 cases split 70% normal / 20% edge / 10% must-refuse, scored by an
independent model + 20% human double-review.
