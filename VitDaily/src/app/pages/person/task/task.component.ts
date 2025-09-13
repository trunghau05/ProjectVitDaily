import { Component } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-task',
  imports: [NavbarComponent, FlexCenterDirective, MatIconModule, CommonModule],
  templateUrl: './task.component.html',
  styleUrl: './task.component.scss'
})
export class TaskComponent {
  isKanban: boolean = true;
  isList: boolean = false;
}
