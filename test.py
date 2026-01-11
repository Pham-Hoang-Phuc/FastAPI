db_tasks = {
    1: {
        "title": "Học FastAPI",
        "description": "Học về Pydantic",
        "priority": "High",
        "status": "Doing",
        "assignee": "An",
        "subtasks": [
            {"title": "Đọc docs", "is_completed": True},
            {"title": "Code thử", "is_completed": False}
        ]
    }
}


def name_2(
    assignee: str,
    status: str
):
    total_tasks = 0
    completed_ratio = 0
    completed = 0
    total_sub = 0
    res = []

    for id, task in db_tasks.items():
        dk_asg = (assignee is None) or (assignee.lower() in task["assignee"].lower())
        
        dk_status = (status is None) or (status == task["status"].lower())

        print(dk_asg)
        print(dk_status)

        if dk_asg and dk_status:
            res.append(task)
            total_tasks += 1

            for subtask in task["subtasks"]:
                total_sub += 1
                if subtask["is_completed"] == True:
                    completed += 1
            
            completed_ratio = completed / total_sub
    
    return {
        "list_of_tasks": res,
        "Total_tasks": total_tasks,
        "completed_ratio": completed_ratio
    }

print(name_2("an", 'doing'))