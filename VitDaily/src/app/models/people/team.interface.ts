export interface Team {
  tm_id: string;
  tm_name: string;
  tm_desc?: string;  
  members: Member[];     
  created_at: string; 
  ws_id: string;
}

export interface Member {
  role: string;        
  us_id: string;       
  us_name?: string;    
  us_img?: string | null;  
  joined_at: string;   
}
