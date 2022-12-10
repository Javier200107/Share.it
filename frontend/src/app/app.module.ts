import { NgModule } from '@angular/core'
import { BrowserModule } from '@angular/platform-browser'
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { AppRoutingModule } from './app-routing.module'
import { HttpClientModule } from '@angular/common/http'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'

import { AppComponent } from './app.component'
import { RegisterComponent } from './components/register/register.component'
import { LoginComponent } from './components/login/login.component'
import { HomeComponent } from './components/home/home.component'
import { ProfileComponent } from './components/profile/profile.component'
import { PostComponent } from './components/post/post.component'
import { CreatePostComponent } from './components/create-post/create-post.component'

import { MatInputModule } from '@angular/material/input'
import { MatFormFieldModule } from '@angular/material/form-field'
import { MatRadioModule } from '@angular/material/radio'
import { MatButtonModule } from '@angular/material/button'
import { MatIconModule } from '@angular/material/icon'
import { MatCardModule } from '@angular/material/card'
import { NavbarComponent } from './components/navbar/navbar.component'
import { MatSlideToggleModule } from '@angular/material/slide-toggle'
import { MatToolbarModule } from '@angular/material/toolbar'
import { MatTabsModule } from '@angular/material/tabs';
import { ProfileUserComponent } from './components/profile-user/profile-user.component';
import { CommunityComponent } from './components/community/community.component'
import { UserSearchComponent } from './components/user-search/user-search.component';
import { UserItemComponent } from './components/user-item/user-item.component'
import {MatSidenavModule} from "@angular/material/sidenav";
import { UserComponent } from './components/user/user.component';
import {DialogModule} from "primeng/dialog";
import {ButtonModule} from "primeng/button";
import { SettingsComponent } from './components/settings/settings.component';
import {AvatarModule} from "primeng/avatar";
import {RippleModule} from "primeng/ripple";
import {InputTextModule} from "primeng/inputtext";
import {CalendarModule} from "primeng/calendar";

@NgModule({
  declarations: [
    AppComponent,
    RegisterComponent,
    LoginComponent,
    HomeComponent,
    ProfileComponent,
    NavbarComponent,
    PostComponent,
    CreatePostComponent,
    ProfileUserComponent,
    CommunityComponent,
    UserSearchComponent,
    UserItemComponent,
    UserComponent,
    SettingsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    MatInputModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatRadioModule,
    MatCardModule,
    MatButtonModule,
    MatSlideToggleModule,
    MatToolbarModule,
    MatIconModule,
    MatTabsModule,
    MatSidenavModule,
    DialogModule,
    ButtonModule,
    AvatarModule,
    RippleModule,
    InputTextModule,
    CalendarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
