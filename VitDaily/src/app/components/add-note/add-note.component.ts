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
  autoResize(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }
  
  formatText(command: string) {
    document.execCommand(command, false);
  }
}
