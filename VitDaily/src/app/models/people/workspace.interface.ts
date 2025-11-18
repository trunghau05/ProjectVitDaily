export interface WorkSpace {
  ws_id: string;          
  ws_name: string;       
  ws_label: string;      
  ws_note?: string;      
  members: Member[];     
  created_at: string;    
  owner_id: string;     
}

export interface Member {
  role: string;        
  us_id: string;       
  us_name?: string;    
  us_img?: string | null;  
  joined_at: string;   
}
