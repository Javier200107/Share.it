import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { RegisterComponent } from './components/register/register.component'
import { LoginComponent } from './components/login/login.component'
import { HomeComponent } from './components/home/home.component'
import { ProfileComponent } from './components/profile/profile.component'
import { PostComponent } from './components/post/post.component'
import {ProfileUserComponent} from "./components/profile-user/profile-user.component";
import {HttpClientModule} from "@angular/common/http";
import {CommunityComponent} from "./components/community/community.component";
import {UserSearchComponent} from "./components/user-search/user-search.component";
import {SettingsComponent} from "./components/settings/settings.component";

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'home', component: HomeComponent },
  { path: 'post', component: PostComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'profileUser', component: ProfileUserComponent },
  { path: 'community', component: CommunityComponent },
  { path: 'userSearch', component: UserSearchComponent },
  { path: 'settings', component: SettingsComponent },
  { path: '', component: RegisterComponent }
  // { path: '**', component: PageNotFoundComponent }
]

@NgModule({
  imports: [RouterModule.forRoot(routes), HttpClientModule],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
