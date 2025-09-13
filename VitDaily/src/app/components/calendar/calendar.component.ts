import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatCalendar } from '@angular/material/datepicker';
import { FlexCenterDirective } from "../../directives/flex-center/flex-center.directive";
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule, MatCalendar, FlexCenterDirective, MatIconModule],
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent {
  tasks = [
    { title: 'Học Angular', date: new Date(2025, 7, 14) },
    { title: 'Viết báo cáo', date: new Date(2025, 7, 16) },
    { title: 'Họp nhóm', date: new Date(2025, 7, 16) },
    { title: 'Báo cáo đồ án', date: new Date(2025, 7, 18) }
  ];
}
