import { Injectable } from '@angular/core';
import axios from 'axios';
import { WorkSpace, Member } from '../../models/people/workspace.interface';

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  apiUrl = 'http://localhost:8000/workspace/member/';

  constructor() { }

  async getMember(ws_id: string | null) {
    try {
      const response = await axios.get(this.apiUrl + 'get/' + ws_id);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }

  async addMembers(data: {ws_id: string, members: Member[]}) {
    try {
      const response = await axios.post(this.apiUrl + 'add/', data);
      return response.data;

    } catch (error) {
      console.error("Add members error:", error);
      throw error;
    }
  }

  async updateMembers(data: {ws_id: string, members: Member[]}) {
    try {
      const response = await axios.put(this.apiUrl + 'update/', data);
      return response.data; 
    } catch (error) {
      console.error("Update members error:", error);
      throw error;
    }
  }

  async removeMember(ws_id: string, us_id: string) {
    try {
      const response = await axios.delete(this.apiUrl + 'delete/' + ws_id + '/' + us_id);
      return response.data;
    } catch (error) {
      console.error("Remove member error:", error);
      throw error;
    }
  }
}
