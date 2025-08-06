import { Component } from '@angular/core';
import { FlexCenterDirective } from '../../directives/flex-center/flex-center.directive';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormatDatePipe } from '../../pipes/format-date/format-date.pipe';

@Component({
  selector: 'app-add-note',
  imports: [FlexCenterDirective, CommonModule, MatIconModule, FormatDatePipe],
  templateUrl: './add-note.component.html',
  styleUrl: './add-note.component.scss'
})
export class AddNoteComponent {
  date = new Date();

  autoResize(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }
}
