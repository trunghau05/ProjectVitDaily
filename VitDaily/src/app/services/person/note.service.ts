import { Injectable } from '@angular/core';
import axios from 'axios';
import { Note } from '../../models/note.interface';

@Injectable({
  providedIn: 'root'
})
export class NoteService {
  apiUrl = 'http://127.0.0.1:8000/note/';

  constructor() { }

  async getNoteList(us_id: string) {
    try {
      const respone = await axios.get(this.apiUrl + 'note-list/' + '?us_id=' + us_id);
      return respone.data;
    } catch (error) {
      return Response.error;
    }
  }

  async getNoteDetail(us_id: string, nt_id: string) {
    try {
      const respone = await axios.get(this.apiUrl + 'detail/' + '?us_id=' + us_id + '&nt_id=' + nt_id);
      return respone.data;
    } catch (error) {
      return Response.error;
    }
  }

  async addNote(data: {nt_id: string; nt_title: string; nt_subtitle?: string | null; nt_content?: string | null; nt_img?: string | null; nt_pdf?: string | null; nt_date: string;  us_id: string;}) {
    try {
      const respone = await axios.post(this.apiUrl + 'add/', data);
      return respone.data;
    } catch (error) {
      return Response.error;
    }
  }

  async updateNote(nt_id: string, data: Note) {
    try {
      const respone = await axios.patch(this.apiUrl + 'update/' + nt_id + '/', data);
      return respone.data;
    } catch (error) {
      return Response.error;
    }
  }

  async deleteNote(nt_id: string | null) {
    try {
      const respone = await axios.delete(this.apiUrl + 'delete/' + nt_id + '/');
      return respone.data;
    } catch (error) {
      return Response.error;
    }
  }
}
