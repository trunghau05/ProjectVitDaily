import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-change-theme',
  imports: [CommonModule, MatIconModule],
  templateUrl: './change-theme.component.html',
  styleUrl: './change-theme.component.scss'
})
export class ChangeThemeComponent {
  constructor(private dialogRef: MatDialogRef<ChangeThemeComponent>) {}

  closeTheme() {
    this.dialogRef.close();
  }
}
