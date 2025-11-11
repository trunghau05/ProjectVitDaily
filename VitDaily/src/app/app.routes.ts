import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { NoteComponent } from './pages/person/note/note.component';
import { ChangeThemeComponent } from './components/change-theme/change-theme.component';
import { AddNoteComponent } from './components/person/add-note/add-note.component';
import { DetailNoteComponent } from './components/person/detail-note/detail-note.component';
import { TaskComponent } from './pages/person/task/task.component';
import { VitaiComponent } from './components/vitai/vitai.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'theme', component: ChangeThemeComponent },
  { path: 'vitai', component: VitaiComponent },

  // Person
  { path: 'note', component: NoteComponent },
  { path: 'add-note', component: AddNoteComponent },
  { path: 'person/task', component: TaskComponent },
  { path: 'person/detail-note/:nt_id', component: DetailNoteComponent },
  
];
