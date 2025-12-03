
export interface Member {
    role: string;        
    us_id: string;       
    us_name?: string;    
    us_img?: string | null;  
    joined_at: string;  
}

export interface Subtask {
    st_id: string;
    st_title: string;
    st_subtitle?: string;
    st_note?: string;
}

export interface Task {
    ts_id: string;
    ts_title: string;
    ts_subtitle?: string;
    ts_status: number;
    ts_start: string;   
    ts_end: string;       
    ts_note?: string;
    owner_id: string;
    tm_id?: string;
    assignees: Member[];    
    subtasks: Subtask[];   
}
