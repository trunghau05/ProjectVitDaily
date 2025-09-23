import axios from 'axios';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  apiUrl = 'http://127.0.0.1:8000/task/';

  constructor() { }
}
