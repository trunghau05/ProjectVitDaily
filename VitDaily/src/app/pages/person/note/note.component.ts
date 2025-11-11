import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { SearchBarComponent } from "../../../components/search-bar/search-bar.component";
import { MatIconModule } from '@angular/material/icon';
import { Note } from '../../../models/note.interface';
import { FormatDatePipe } from '../../../pipes/format-date/format-date.pipe';
import { CommonModule } from '@angular/common';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { Router } from '@angular/router';
import { NoteService } from '../../../services/person/note.service';
import { VitaiComponent } from '../../../components/vitai/vitai.component';

@Component({
  selector: 'app-note',
  imports: [NavbarComponent, MatIconModule, SearchBarComponent, FormatDatePipe, CommonModule, FlexCenterDirective, VitaiComponent],
  templateUrl: './note.component.html',
  styleUrl: './note.component.scss' 
})
export class NoteComponent implements OnInit{
  notes: Note[] = [];
  searchedNotes: Note[] = [];
  displayedNotes: Note[] = []; 

  ntId: string = '';

  isSearch = true;
  isFilter = true;
  isConfirm = false;

  itemPer = 15;
  currentPage = 1;
  totalPages = 2;

  selects = [
    { options: ['A-Z', 'Z-A'], index: -1, label: 'A-Z', active: false },
    { options: ['Mới nhất', 'Cũ nhất'], index: -1, label: 'Mới nhất', active: false },
    { options: ['Ngày', 'Tuần', 'Tháng', 'Năm'], index: -1, label: 'Ngày', active: false }
  ];

  constructor(private router: Router, private noteService: NoteService) {}

  async ngOnInit() {
    this.notes = await this.noteService.getNoteList(sessionStorage.getItem('us_id') || '');
    this.searchedNotes = [...this.notes];
    this.updateTotalPages();
    this.loadPage(this.currentPage);
  }

  onSearch(keyword: string) {
    const lowerKeyword = keyword.toLowerCase();
    this.searchedNotes = this.notes.filter(note =>
      note.nt_title.toLowerCase().includes(lowerKeyword) ||
      (note.nt_subtitle?.toLowerCase().includes(lowerKeyword)) ||
      (note.nt_content?.toLowerCase().includes(lowerKeyword)) ||
      (note.nt_date?.toLowerCase().includes(lowerKeyword))
    );
    this.currentPage = 1;
    this.updateTotalPages();
    this.loadPage(this.currentPage);
  }

  toggleSearch() {
    this.isSearch = !this.isSearch;
  }
  
  toggleFilter() {
    this.isFilter = !this.isFilter;
  }

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }

  detailNote(nt_id: string) {
    this.router.navigate(['person/detail-note', nt_id]);
  }

  filterOption(i: number) {
    const select = this.selects[i];
    const totalOptions = select.options.length;

    if (select.index === -1) {
      select.index = 0;
      select.active = true;
    }
    else if (select.index < totalOptions - 1) {
      select.index++;
    }
    else {
      select.index = -1;
      select.active = false;
    }

    select.label = select.index === -1 ? select.options[0] : select.options[select.index];

    this.applyFilters();
  }

  applyFilters() {
    let filtered = [...this.notes];

    const azSelect = this.selects[0];
    if (azSelect.index !== -1) {
      if (azSelect.options[azSelect.index] === 'A-Z') {
        filtered.sort((a, b) => a.nt_title.localeCompare(b.nt_title));
      } else if (azSelect.options[azSelect.index] === 'Z-A') {
        filtered.sort((a, b) => b.nt_title.localeCompare(a.nt_title));
      }
    }

    const sortSelect = this.selects[1];
    if (sortSelect.index !== -1) {
      if (sortSelect.options[sortSelect.index] === 'Mới nhất') {
        filtered.sort((a, b) => new Date(b.nt_date).getTime() - new Date(a.nt_date).getTime());
      } else if (sortSelect.options[sortSelect.index] === 'Cũ nhất') {
        filtered.sort((a, b) => new Date(a.nt_date).getTime() - new Date(b.nt_date).getTime());
      }
    }

    const dateSelect = this.selects[2];
    if (dateSelect.index !== -1) {
      const now = new Date();
      if (dateSelect.options[dateSelect.index] === 'Ngày') {
        filtered = filtered.filter(n => {
          const noteDate = new Date(n.nt_date);
          return noteDate.toDateString() === now.toDateString();
        });
      }
      else if (dateSelect.options[dateSelect.index] === 'Tuần') {
        const now = new Date();
        const day = now.getDay(); 
        
        const monday = new Date(now);
        monday.setDate(now.getDate() - (day === 0 ? 6 : day - 1));
        monday.setHours(0, 0, 0, 0);

        const sunday = new Date(monday);
        sunday.setDate(monday.getDate() + 6);
        sunday.setHours(23, 59, 59, 999);

        filtered = filtered.filter(n => {
          const noteDate = new Date(n.nt_date);
          return noteDate >= monday && noteDate <= sunday;
        });
      }
      else if (dateSelect.options[dateSelect.index] === 'Tháng') {
        filtered = filtered.filter(n => {
          const noteDate = new Date(n.nt_date);
          return noteDate.getMonth() === now.getMonth() &&
                noteDate.getFullYear() === now.getFullYear();
        });
      }
      else if (dateSelect.options[dateSelect.index] === 'Năm') {
        filtered = filtered.filter(n => {
          const noteDate = new Date(n.nt_date);
          return noteDate.getFullYear() === now.getFullYear();
        });
      }
    }

    this.searchedNotes = filtered;
    this.currentPage = 1;
    this.updateTotalPages();
    this.loadPage(this.currentPage);
  }

  loadPage(page: number) {
    const start = (page - 1) * this.itemPer;
    const end = page * this.itemPer;
    this.displayedNotes = this.searchedNotes.slice(start, end);
  }

  updateTotalPages() {
    this.totalPages = Math.ceil(this.searchedNotes.length / this.itemPer) || 1;
    if (this.currentPage > this.totalPages) this.currentPage = this.totalPages;
  }

  changePage(page: number) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadPage(this.currentPage);
    }
  }

  nextPage() {
    if (this.currentPage < this.totalPages) this.currentPage++;
    this.loadPage(this.currentPage);
  }

  prevPage() {
    if (this.currentPage > 1) this.currentPage--;
    this.loadPage(this.currentPage);
  }
}