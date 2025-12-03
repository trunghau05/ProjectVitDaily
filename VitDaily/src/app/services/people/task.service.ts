import { Injectable } from '@angular/core';
import axios from 'axios';
import { Task } from '../../models/people/task.interface';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  apiUrl = 'http://localhost:8000/task/people/';

  constructor() { }

  async getTaskList(tm_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'get/' + tm_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async getTaskDetail(ts_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'detail/' + ts_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async addTasks(tasks: Task[]) {
    try {
      const response = await axios.post(this.apiUrl + 'add/', tasks);
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  async deleteTask(ts_id: string | null=null) {
    try {
      const response = await axios.delete(this.apiUrl + 'delete/' + ts_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async updateTask(ts_id: string | null = null, data: Task) {
    try {
      const response = await axios.put(this.apiUrl + 'update/' + ts_id + '/', data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}
