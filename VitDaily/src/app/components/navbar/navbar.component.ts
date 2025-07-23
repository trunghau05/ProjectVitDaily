import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  imports: [CommonModule, MatIconModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  isPersonOpen = false;
  isPeopleOpen = false;
  
  constructor(private router: Router) {}

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
}
