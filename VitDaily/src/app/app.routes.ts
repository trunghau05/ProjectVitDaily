import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { NoteComponent } from './pages/person/note/note.component';
import { ChangeThemeComponent } from './components/change-theme/change-theme.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'note', component: NoteComponent },
  { path: 'theme', component: ChangeThemeComponent },
];
