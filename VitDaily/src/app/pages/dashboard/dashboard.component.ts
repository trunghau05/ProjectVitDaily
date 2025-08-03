import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { NavbarComponent } from '../../components/navbar/navbar.component';
import { BreadCrumbComponent } from "../../components/bread-crumb/bread-crumb.component";

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, MatIconModule, NavbarComponent, BreadCrumbComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  
}
