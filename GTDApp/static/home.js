//NOTE: Temporary, stub API connection until we get a real one going
const APIUtil = {
    get(url){
        return fetch(url, {
            cache: "no-cache",
            credentials: "same-origin",
            method: "GET",
            mode: "cors",
            redirect: "follow",
            referrer: "no-referrer"
        }).then(res => res.json());
    },
    post(url, data){
        return fetch(url, {
            body: JSON.stringify(data),
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "content-type": "application/json"
            },
            method: "POST",
            mode: "cors",
            redirect: "follow",
            referrer: "no-referrer"
        }).then(res => res.json());
    }
};

const APIConn = {
    addNewItem(itemDescription){
        return APIUtil.post("/api/item", {description: itemDescription});
    },
    addNewTask(taskDescription){
        return APIUtil.post("/api/task", {description: taskDescription});
    },
    addNewProject(projectDescription){
        //TODO
        return;
    },
    delete(mode, id){
        const url = `/api/${mode}/delete/${id}`;
        return APIUtil.post(url, {id: id});
    },
    itemToTask(id){
        return new Promise((resolve, reject) => {
            resolve({
                id: Math.floor(Math.random() * 150),
                description: app.items.filter(i => i.id === id)[0].description,
                status: "todo"
            });
        });
    },
    itemToProject(id){
        return new Promise((resolve, reject) => {
            resolve({
                id: Math.floor(Math.random() * 150),
                description: app.items.filter(i => i.id === id)[0].description,
                tasks: []
            });
        });
    },
    addProjectSubtask(pid, description){
        return new Promise((resolve, reject) => {
            resolve({
                id: Math.floor(Math.random() * 150),
                description,
                status: "todo"
            });
        });
    },
    toggleTaskStatus(task){
        return new Promise((resolve, reject) => {
            let newStatus;
            if(task.status === "todo"){
                newStatus = "done";
            } else {
                newStatus = "todo";
            }
            resolve({
                id: task.id,
                description: task.description,
                status: newStatus
            });
        });
    },
    getAllItems(){
        return APIUtil.get("/api/item");
    },
    getAllTasks(){
        return APIUtil.get("/api/task");
    }
};

const app = new Vue({
    el: '#app',
    data: {
        mode: 0,
        modeStrs: ["Inbox", "Someday/Maybe", "Tasks", "Projects"],
        newGTDThing: "", //TODO: Make this less generic `thing`
        newGTDSubtask: "",
        focusedProjectID: "",
        // TODO: Unhardcode this stuff once we have the api
        items: [],
        tasks: [],
        projects: [
            {id: "9", description: "Project A", tasks:[]},
            {id: "10",
                description: "Project B",
                tasks:[
                    {id: "12", description: "Project A Task 1", status: "next"},
                    {id: "13", description: "Project A Task 2", status: "todo"},
                ]
            },
            {id: "11", description: "Project C",
                tasks:[
                    {id: "14", description: "Project C Task 1", status: "todo"},
                ]
            },
        ]
    },
    mounted: function(){
        //TODO: Promise.all or async/await this thing
        APIConn.getAllItems()
            .then(res => {
                if(res.success){
                    this.items = res.data;
                }
            })
            .then(() => {
                return APIConn.getAllTasks();
            })
            .then(res => {
                if(res.success){
                    this.tasks = res.data;
                }
            });
    },
    computed: {
        modeStr(){
            return this.computeModeStr();
        }
    },
    methods: {
        //TODO: Create a generic number-wrap function for both toggle-forward and toggle-backward
        toggleModeForward(){
            this.mode = (this.mode + 1) % this.modeStrs.length; 
        },
        toggleModeBackward(){
            this.mode = (this.mode - 1);
            if(this.mode < 0){
                this.mode = this.modeStrs.length - 1;
            }
        },
        computeModeStr(mode=null){
            const mode_compute = mode ? mode : this.mode;
            return this.modeStrs[mode_compute];
        },
        addGTDThing(){
            const mode = this.mode;
            let APIFunc, listType;
            switch (mode){
                case 0:
                case 1:
                    APIFunc = APIConn.addNewItem;
                    listType = "items";
                    break;
                case 2:
                    APIFunc = APIConn.addNewTask;
                    listType = "tasks";
                    break;
                case 3:
                    APIFunc = APIConn.addNewProject;
                    listType = "projects";
                    break;
            }
            if(this.newGTDThing.length <= 0)
                return;
            APIFunc(this.newGTDThing)
                .then((res) => {
                    if(res.success){
                        this.newGTDThing = "";
                        this[listType].push(res.data);
                    }
                });
        },
        deleteGTDThing(mode, id){
            //TODO: Improve this code
            const properties = ["items", "items", "tasks", "projects"];
            const api_call = ["item", "item", "task", "project"];
            APIConn.delete(api_call[mode], id).then(res => {
                if(res.success){
                    const filtered_list = [];
                    for(let i = 0; i < this[properties[mode]].length; i++){
                        let filtered_item = Object.assign({}, this[properties[mode]][i]);
                        if(filtered_item.tasks){
                            let new_tasks = [];
                            for(let j = 0; j < filtered_item.tasks.length; j++){
                                if(filtered_item.tasks[j].id !== id){new_tasks.push(filtered_item.tasks[j]);}
                            }
                            filtered_item.tasks = new_tasks;
                        }
                        if (filtered_item.id !== id){
                            filtered_list.push(filtered_item);
                        }
                    }
                    this[properties[mode]] = filtered_list;
                }
            });
        },
        itemToTask(id){
            APIConn.itemToTask(id).then(res => {
                this.items = this.items.filter(i => i.id !== id);
                this.tasks.push(res);
            });
        },
        itemToProject(id){
            APIConn.itemToProject(id).then(res => {
                this.items = this.items.filter(i => i.id !== id);
                this.projects.push(res);
            });
        },
        focusProject(id){
            this.newGTDSubtask = "";
            this.focusedProjectID = id;
        },
        noFocusProject(){
            this.newGTDSubtask = "";
            this.focusedProjectID = "";
        },
        addProjectSubtask(){
            const projectID = this.focusedProjectID;
            const subtask = this.newGTDSubtask;
            if(subtask.length === 0)
                return;
            APIConn.addProjectSubtask(projectID, subtask).then((res) => {
                this.noFocusProject();
                this.projects = this.projects.map((p) => {
                    if(p.id !== projectID){
                        return p;
                    }
                    return Object.assign({}, p, {tasks: p.tasks.concat(res)});
                });
            });
        },
        toggleTaskStatus(mode, task){
            const properties = ["items", "items", "tasks", "projects"];
            APIConn.toggleTaskStatus(task).then((updatedTask) => {
                task.status = updatedTask.status;
            });
        }
    }
});
