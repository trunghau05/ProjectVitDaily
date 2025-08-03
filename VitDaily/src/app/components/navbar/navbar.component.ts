import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ChangeThemeComponent } from '../change-theme/change-theme.component';

@Component({
  selector: 'app-navbar',
  imports: [CommonModule, MatIconModule, ChangeThemeComponent],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent implements OnInit {
  isPersonOpen = false;
  isPeopleOpen = false;
  isThemeOpen = false
  
  constructor(private router: Router, private dialog: MatDialog) {}

  ngOnInit() {
    const route = this.router.url;
    if (route.includes('/note') || route.includes('/task')) {
      this.isPersonOpen = true;
    }
  }

  togglePerson() {
    this.isPersonOpen = !this.isPersonOpen;
    this.isPeopleOpen = false; 
  }

  togglePeople() {
    this.isPeopleOpen = !this.isPeopleOpen;
    this.isPersonOpen = false;
  }

  isActive(route: string): boolean {  
    return this.router.url === `/${route}`;
  }

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }

  openTheme() {
    this.dialog.open(ChangeThemeComponent);
  }
}
