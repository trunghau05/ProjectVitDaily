import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { FlexCenterDirective } from '../../directives/flex-center/flex-center.directive';
import { FormsModule } from '@angular/forms';
import { FormatDatePipe } from '../../pipes/format-date/format-date.pipe';
import { NavbarComponent } from '../navbar/navbar.component';
import { ActivatedRoute } from '@angular/router';
import { NoteService } from '../../services/person/note.service';
import { Note } from '../../models/note.interface';
import { Location } from '@angular/common';

@Component({
  selector: 'app-detail-note',
  imports: [MatIconModule, CommonModule, FlexCenterDirective, FormsModule, FormatDatePipe, NavbarComponent],
  templateUrl: './detail-note.component.html',
  styleUrl: './detail-note.component.scss'
})
export class DetailNoteComponent implements OnInit {
  date = new Date();
  noteId: string | null = null;
  userId: string | null = null;

  note = {} as Note;
  newNote = {} as Note;

  constructor(private route: ActivatedRoute, private noteService: NoteService, private location: Location) {}

  ngOnInit() {
      this.noteId = this.route.snapshot.paramMap.get('nt_id');
      this.userId = sessionStorage.getItem('us_id');
      this.detailNote();
  }

  autoResize(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }

  async detailNote() {
    try {
      const respone = await this.noteService.getNoteDetail(this.userId!, this.noteId!);
      this.note = respone[0];
      this.newNote = this.note;
      console.log(this.newNote);
    } catch (error) {
      console.error(error);
    }
  }

  close() {
    this.location.back();
  }

  async updateNote() {
    try {
      const response = await this.noteService.updateNote(this.noteId!, this.newNote); 
      console.log(response);
      alert('Cập nhật ghi chú thành công!');
      this.close();
    } catch (error) {
      console.error(error);
      alert('Cập nhật ghi chú thất bại!');
    }
  }
}
