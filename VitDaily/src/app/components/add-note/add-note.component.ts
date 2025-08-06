import { Component } from '@angular/core';
import { FlexCenterDirective } from '../../directives/flex-center/flex-center.directive';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-add-note',
  imports: [FlexCenterDirective, CommonModule],
  templateUrl: './add-note.component.html',
  styleUrl: './add-note.component.scss'
})
export class AddNoteComponent {
  
}
