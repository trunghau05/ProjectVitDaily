import { Injectable } from '@angular/core';
import axios from 'axios';
import { WorkSpace } from '../../models/people/workspace.interface';

@Injectable({
  providedIn: 'root'
})
export class WorkspaceService {
  apiUrl = 'http://localhost:8000/workspace/';

  constructor() { }

  async getWorkspaceOwner(us_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'is-owner/' + '?us_id=' + us_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async getWorkspaceMember(us_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'is-member/' + '?us_id=' + us_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async addWorkspace(data: WorkSpace) {
    try {
      const response = await axios.post(this.apiUrl + 'add/', data);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async getWorkspaceDetail(ws_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'detail/' + '?ws_id=' + ws_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async updateWorkspace(data: WorkSpace) {
    try {
      const response = await axios.put(this.apiUrl + 'update/', data);
      return response.data;
    } catch (error) {
      Response.error;
    }   
  }

}
