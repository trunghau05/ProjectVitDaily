import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { NavbarComponent } from '../../components/navbar/navbar.component';
import { CalendarComponent } from '../../components/calendar/calendar.component';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, MatIconModule, NavbarComponent, CalendarComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  ngOnInit(): void {
      sessionStorage.setItem('us_id', 'US001');
  }
}
