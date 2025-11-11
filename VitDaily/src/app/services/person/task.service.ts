import axios from 'axios';
import { Injectable } from '@angular/core';
import { Task } from '../../models/task.interface';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  apiUrl = 'http://127.0.0.1:8000/task/person/';

  constructor() { }

  async addTask(data: {ts_title: string, ts_subtitle: string, ts_status: string, ts_start: Date, ts_end: Date, ts_note: string, us_id: string, ws_id: string}) {
    try {
      const respone = await axios.post(this.apiUrl + 'add/', data);
      return respone.data;
    } catch (error) {
      return Response.error;
    }
  }

  async getTaskList(us_id: string) {
    try {
      const respone = await axios.get(this.apiUrl + 'task-list/' + '?us_id=' + us_id);
      return respone.data;
    } catch (error) {
      Response.error;
    }
  }

  async taskDetail(ts_id: string | null) {
    try {
      const respone = await axios.get(this.apiUrl + 'task-detail' + '?ts_id=' + ts_id);
      return respone.data;
    } catch (error) {
      Response.error;
    }
  }

  async updateTask(ts_id: string, data: Task) {
    try {
      const respone = await axios.patch(this.apiUrl + 'update/' + ts_id + '/', data);
      return respone.data;
    } catch (error) {
      Response.error;
    }
  }
}
