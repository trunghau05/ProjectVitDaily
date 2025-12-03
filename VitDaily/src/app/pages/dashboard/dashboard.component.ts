import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { NavbarComponent } from '../../components/navbar/navbar.component';
import { FlexCenterDirective } from "../../directives/flex-center/flex-center.directive";

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, MatIconModule, NavbarComponent, FlexCenterDirective],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  ngOnInit(): void {
      sessionStorage.setItem('us_id', 'US001');
  }
}
