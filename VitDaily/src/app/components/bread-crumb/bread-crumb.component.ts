import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-bread-crumb',
  imports: [CommonModule],
  templateUrl: './bread-crumb.component.html',
  styleUrl: './bread-crumb.component.scss'
})
export class BreadCrumbComponent {
  constructor(private router: Router) {}

  breadcrumbs = [
    { label: 'Apps', route: 'apps' },
    { label: 'Dashboards', route: 'apps/dashboards' },
    { label: 'Overview', route: 'apps/dashboards/overview' }
  ];

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }

  isActive(route: string): boolean {
    return this.router.url === `/${route}`;
  }
}
