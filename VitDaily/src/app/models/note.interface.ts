export interface Note {
  nt_id: string;
  nt_title: string;
  nt_subtitle?: string | null;
  nt_content?: string | null;
  nt_img?: string | null;
  nt_pdf?: string | null;
  nt_date: string; 
  us_id: string;
}