import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { SearchBarComponent } from "../../../components/search-bar/search-bar.component";
import { MatIconModule } from '@angular/material/icon';
import { Note } from '../../../models/note/note';
import { FormatDatePipe } from '../../../pipes/format-date/format-date.pipe';
import { CommonModule } from '@angular/common';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { Router } from '@angular/router';

@Component({
  selector: 'app-note',
  imports: [NavbarComponent, MatIconModule, SearchBarComponent, FormatDatePipe, CommonModule, FlexCenterDirective],
  templateUrl: './note.component.html',
  styleUrl: './note.component.scss' 
})
export class NoteComponent implements OnInit{
  notes: Note[] = [];
  searchedNotes: Note[] = [];

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
        us_id: 'Nguyễn Văn A'
      },
      {
        nt_id: 'NT002',
        nt_title: 'Django REST API',
        nt_subtitle: 'Kết nối với Angular',
        nt_content: 'Hướng dẫn tạo API cho model Note trong Django.',
        nt_img: null,
        nt_pdf: 'https://example.com/file.pdf',
        nt_date: '2025-08-05T15:30:00Z',
        us_id: 'Hà Thị B'
      },
      {
        nt_id: 'NT003',
        nt_title: 'Test dữ liệu mẫu',
        nt_subtitle: null,
        nt_content: 'Dùng dữ liệu này để test hiển thị trong component Angular.',
        nt_img: null,
        nt_pdf: null,
        nt_date: '2025-08-09T08:45:00Z',
        us_id: 'Trần Hoàng B'
      },
      {
        nt_id: 'NT004',
        nt_title: 'Ionic UI Components',
        nt_subtitle: 'Thiết kế giao diện đẹp',
        nt_content: 'Học cách sử dụng các component của Ionic để tạo giao diện hiện đại.',
        nt_img: 'https://example.com/image2.jpg',
        nt_pdf: null,
        nt_date: '2025-08-10T09:15:00Z',
        us_id: 'Phạm Minh C'
      },
      {
        nt_id: 'NT005',
        nt_title: 'Firebase Realtime Database',
        nt_subtitle: 'Đồng bộ dữ liệu',
        nt_content: 'Kết nối và đồng bộ dữ liệu giữa Angular và Firebase theo thời gian thực.',
        nt_img: null,
        nt_pdf: 'https://example.com/firebase-guide.pdf',
        nt_date: '2025-08-11T14:20:00Z',
        us_id: 'Ngô Thị D'
      },
      {
        nt_id: 'NT006',
        nt_title: 'MySQL Query nâng cao',
        nt_subtitle: 'Truy vấn tối ưu',
        nt_content: 'Các kỹ thuật viết query MySQL nâng cao để tối ưu tốc độ xử lý.',
        nt_img: null,
        nt_pdf: null,
        nt_date: '2025-08-12T07:50:00Z',
        us_id: 'Lê Văn E'
      },
      {
        nt_id: 'NT007',
        nt_title: 'Bảo mật thông tin',
        nt_subtitle: 'Trong ứng dụng web',
        nt_content: 'Những cách bảo mật dữ liệu và phòng chống tấn công XSS, CSRF.',
        nt_img: 'https://example.com/image3.jpg',
        nt_pdf: null,
        nt_date: '2025-08-13T16:40:00Z',
        us_id: 'Đỗ Thị F'
      },
      {
        nt_id: 'NT008',
        nt_title: 'Triển khai ứng dụng',
        nt_subtitle: 'Deploy Django + Angular',
        nt_content: 'Hướng dẫn triển khai ứng dụng Django backend và Angular frontend lên server.',
        nt_img: null,
        nt_pdf: 'https://example.com/deploy-doc.pdf',
        nt_date: '2025-08-14T11:05:00Z',
        us_id: 'Bùi Quốc G'
      },
      {
        nt_id: 'NT009',
        nt_title: 'Git Workflow',
        nt_subtitle: 'Quản lý code nhóm',
        nt_content: 'Học cách sử dụng Git Flow để quản lý quá trình phát triển phần mềm trong nhóm.',
        nt_img: 'https://example.com/image4.jpg',
        nt_pdf: null,
        nt_date: '2025-08-15T13:30:00Z',
        us_id: 'Vũ Hoàng H'
      },
      {
        nt_id: 'NT010',
        nt_title: 'Unit Test với Jest',
        nt_subtitle: 'Kiểm thử Angular',
        nt_content: 'Viết test case và chạy kiểm thử đơn vị cho ứng dụng Angular với Jest.',
        nt_img: null,
        nt_pdf: 'https://example.com/jest-testing.pdf',
        nt_date: '2025-08-16T10:10:00Z',
        us_id: 'Nguyễn Thị L'
      }
    ];
    this.searchedNotes = [...this.notes];
  }

  constructor(private router: Router) {}

  onSearch(keyword: string) {
    const lowerKeyword = keyword.toLowerCase();
    this.searchedNotes = this.notes.filter(note =>
      note.nt_title.toLowerCase().includes(lowerKeyword) ||
      (note.nt_subtitle?.toLowerCase().includes(lowerKeyword)) ||
      (note.nt_content?.toLowerCase().includes(lowerKeyword)) ||
      (note.nt_date?.toLowerCase().includes(lowerKeyword))
    );
  }

  toggleSearch() {
    this.isSearch = !this.isSearch;
  }

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }
}
