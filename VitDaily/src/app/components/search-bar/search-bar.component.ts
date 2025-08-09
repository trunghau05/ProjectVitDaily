// search-bar.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { FlexCenterDirective } from '../../directives/flex-center/flex-center.directive';

@Component({
  selector: 'app-search-bar',
  standalone: true,
  imports: [MatIconModule, CommonModule, FlexCenterDirective],
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.scss'
})
export class SearchBarComponent {
  @Input() placeholder = '';
  @Output() searchChange = new EventEmitter<string>();

  onSearch(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.searchChange.emit(value);
  }
}
