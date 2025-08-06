import { Component } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { AddNoteComponent } from '../../../components/add-note/add-note.component';

@Component({
  selector: 'app-note',
  imports: [NavbarComponent, AddNoteComponent],
  templateUrl: './note.component.html',
  styleUrl: './note.component.scss'
})
export class NoteComponent {

}
