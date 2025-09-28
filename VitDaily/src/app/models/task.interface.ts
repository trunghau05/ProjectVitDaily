export interface Task {
  ts_id: string;           
  ts_title: string;        
  ts_subtitle?: string;  
  ts_status: number;       
  ts_start: string;        
  ts_end: string;          
  ts_note?: string;         
  us_id: string;            
  ws_id?: string | null;    
}
