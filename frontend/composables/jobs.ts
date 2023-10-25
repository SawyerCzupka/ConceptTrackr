
import {defineStore} from "pinia";

export const useJobsStore = defineStore('jobs', {
    state: () => {
        return { jobs: ['task-id-0']}
    },
    actions: {
        add_task() {
            this.jobs.push("new task");
        }
    }
});