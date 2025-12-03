import { Injectable } from '@angular/core';
import axios from 'axios';
import { WorkSpace } from '../../models/people/workspace.interface';
import { Team } from '../../models/people/team.interface';

@Injectable({
  providedIn: 'root'
})
export class TeamService {
  apiUrl = 'http://localhost:8000/team/';

  constructor() { }

  async getTeamByWorkspace(ws_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'get/' + '?ws_id=' + ws_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async getTeamDetail(tm_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'detail/' + '?tm_id=' + tm_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async addTeam(data: Team) {
    try {
      const response = await axios.post(this.apiUrl + 'add/', data);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async updateTeam(tm_id: string | null=null, data: Team) {
    try {
      const response = await axios.put(this.apiUrl + 'update/' + tm_id, data);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async deleteTeam(tm_id: string | null=null) {
    try {
      const response = await axios.delete(this.apiUrl + 'delete/' + tm_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

}
