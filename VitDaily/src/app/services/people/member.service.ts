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

  async addMember(data: Member) {
    try {
      const response = await axios.post(this.apiUrl + 'add/', data);
      return response.data;
    } catch (error) {
      Response.error;
    }
  }
}
