import { Component } from '@angular/core';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormatDatePipe } from '../../../pipes/format-date/format-date.pipe';
import { NavbarComponent } from '../../navbar/navbar.component';
import { FormsModule } from "@angular/forms";
import { Note } from '../../../models/note.interface';
import { NoteService } from '../../../services/person/note.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-add-note',
  imports: [FlexCenterDirective, CommonModule, MatIconModule, FormatDatePipe, NavbarComponent, FormsModule],
  templateUrl: './add-note.component.html',
  styleUrl: './add-note.component.scss'
})
export class AddNoteComponent {
  date = new Date();
  newNote: Note = {
    nt_id: '',
    nt_title: '',
    nt_subtitle: null,
    nt_content: null,
    nt_img: null,
    nt_pdf: null,
    nt_date: new Date().toISOString(),
    us_id: 'US001'
  };

  constructor(private noteService: NoteService, private location: Location) {}

  autoResize(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }

  async addNote() {
    try {
      const response = await this.noteService.addNote(this.newNote);
      alert(response.message);
      this.location.back();
    } catch (error) {
      alert(Response.error);
    }
  }
}
