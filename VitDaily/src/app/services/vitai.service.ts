import axios from 'axios';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class VitaiService {
    apiUrl = 'http://127.0.0.1:8000/vitai/';

    constructor() { }

    async chatVitai(us_input: string, us_id: string | null=null) {
        try {
            const response = await axios.post(this.apiUrl, { us_input: us_input, us_id: us_id });
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}