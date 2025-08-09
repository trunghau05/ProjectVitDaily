import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { SearchBarComponent } from "../../../components/search-bar/search-bar.component";
import { MatIconModule } from '@angular/material/icon';
import { Note } from '../../../models/note/note';
import { FormatDatePipe } from '../../../pipes/format-date/format-date.pipe';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-note',
  imports: [NavbarComponent, MatIconModule, SearchBarComponent, FormatDatePipe, CommonModule],
  templateUrl: './note.component.html',
  styleUrl: './note.component.scss'
})
export class NoteComponent implements OnInit{
  notes: Note[] = [];
  filteredNotes: Note[] = [];

  isSearch = false;

  ngOnInit(): void {
    this.notes = [
      {
        nt_id: 'NT001',
        nt_title: 'Học Angular',
        nt_subtitle: 'Interface và TypeScript',
        nt_content: 'Tìm hiểu cách dùng interface để quản lý dữ liệu.',
        nt_img: 'https://example.com/image1.jpg',
        nt_pdf: null,
        nt_date: '2025-08-01T10:00:00Z',
        us_id: 'US001'
      },
      {
        nt_id: 'NT002',
        nt_title: 'Django REST API',
        nt_subtitle: 'Kết nối với Angular',
        nt_content: 'Hướng dẫn tạo API cho model Note trong Django.',
        nt_img: null,
        nt_pdf: 'https://example.com/file.pdf',
        nt_date: '2025-08-05T15:30:00Z',
        us_id: 'US002'
      },
      {
        nt_id: 'NT003',
        nt_title: 'Test dữ liệu mẫu',
        nt_subtitle: null,
        nt_content: 'Dùng dữ liệu này để test hiển thị trong component Angular.',
        nt_img: null,
        nt_pdf: null,
        nt_date: '2025-08-09T08:45:00Z',
        us_id: 'US001'
      }
    ];
    this.filteredNotes = [...this.notes];
  }

  onSearch(keyword: string) {
    const lowerKeyword = keyword.toLowerCase();
    this.filteredNotes = this.notes.filter(note =>
      note.nt_title.toLowerCase().includes(lowerKeyword) ||
      (note.nt_subtitle?.toLowerCase().includes(lowerKeyword)) ||
      (note.nt_content?.toLowerCase().includes(lowerKeyword)) ||
      (note.nt_date?.toLowerCase().includes(lowerKeyword))
    );
  }

  toggleSearch() {
    this.isSearch = !this.isSearch;
  }
}
