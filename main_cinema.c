// favorite_list_size

#ifdef _WIN32
    // библиотеки для windows
    #include <windows.h>
#endif
#ifdef linux
    // библиотеки для linux
#endif
// библиотеки для всех ОС
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <stdbool.h>
#include <dirent.h>
// собственные библиотеки
#include "strings.h"
#include "doubly_linked_looped_list.h"
#include "csv.h"
#include "print.h"

struct session {
    char *login;
    char *card;
    char *pass;
    bool is_admin;
    char *working_dir;
    struct list *films_list;
    struct list *user_favorites_list;
    struct list *users_list;
    uint8_t prev_screen_out_settings;
};

char input() {
    // TODO input()
    // Возвращает посимвольно перехваченный ввод
    char chr;
    #ifdef _WIN32
        chr = getchar();
    #endif

    #ifdef linux
        #include <termios.h>
        static struct termios oldt, newt;
        tcgetattr(STDIN_FILENO, &oldt);
        newt = oldt;
        newt.c_lflag &= ~(ICANON);
        tcsetattr(STDIN_FILENO, TCSANOW, &newt);
        chr = getchar();
        tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    #endif
    return chr;
}

void create_user(struct session *session) {
    // Добавляет пользователя из session в список пользователей и файл пользователей
    session->user_favorites_list = list_create();
    // Добавление в список пользователей
    char *login = (char *) malloc(string_len(session->login) + 1);
    char *card = (char *) malloc(16 + 1);
    char *pass = (char*) malloc(string_len(session->pass) + 1);
    if (NULL == login || NULL == card || NULL == pass) {
        exit(77001);
    }
    for (size_t i = 0; i < string_len(session->login); i++) {
        login[i] = session->login[i];
    }
    login[string_len(session->login)] = '\0';
    for (size_t i = 0; i < 16; i++) {
        card[i] = session->card[i];
    }
    card[16] = '\0';
    for (size_t i = 0; i < string_len(session->pass); i++) {
        pass[i] = session->pass[i];
    }
    pass[string_len(session->pass)] = '\0';
    void *data = data_user_create(login, card, pass, session->is_admin);
    // добавление в файл: выделение памяти для массива полей
    char **array = (char **) malloc(sizeof(char *) * 4);
    if (NULL == array) {
        exit(77001);
    }
    array[0] = login;
    array[1] = card;
    array[2] = pass;
    array[3] = (session->is_admin) ? "1" : "0";
    // запись в файл
    char *path = concatenation(session->working_dir, "users.csv");
    cvs_add(path, 4, array);
    // освобождение памяти
    free(array);
    free(path);
}

bool is_card_valid(char *card) {
    // Проверка строки, что она представляет банковскую карту
    if (NULL == card) {
        exit(77001);
    }
    if (string_len(card) != 16) {
        return false;
    }
    return true;
}

bool is_pass_valid(char *pass) {
    // Проверка, что получаемая строка длиннее 6, имеет как минимум одну латинские заглавную, строчную буквы и цифру.
    if (NULL == pass) {
        exit(77001);
    }
    if (string_len(pass) < 6) {
        return false;
    }
    uint8_t count_n = 0, count_A = 0, count_a = 0;
    for (size_t i = 0; pass[i] != '\0'; i++) {
        if (pass[i] >= 48 && pass[i] <= 57) {
            count_n += 1;
        } else if (pass[i] >= 65 && pass[i] <= 90) {
            count_A += 1;
        } else if (pass[i] >= 97 && pass[i] <= 122) {
            count_a += 1;
        }
    }
    if (count_n < 1 || count_A < 1 || count_a < 1) {
        return false;
    }
    return true;
}

void from_favorites(struct session *session, struct film *film) {
    // Удаляет фильм из списка избранного и из файла текущего пользователя
    if (NULL == session || NULL == film) {
        exit(77004);
    }
    // удаление из списка
    list_remove_film(session->user_favorites_list, film->name, false);
    // удаление из файла
    char *file_name = concatenation(session->login, "_films.csv");
    char *file_path = concatenation(session->working_dir, file_name);
    cvs_remove(file_path, film->name);
    free(file_name);
    free(file_path);
}

void to_favorites(struct session *session, struct film *film) {
    // Добавляет фильм в список избранного и в файл текущего пользователя.
    if (NULL == session || NULL == film) {
        exit(77004);
    }
    // добавление в список
    list_add(session->user_favorites_list, film);
    // добавление в файл: выделение памяти для массива полей
    char **array = (char **) malloc(sizeof(char *) * 6);
    if (NULL == array) {
        exit(77001);
    }
    array[0] = (char *) malloc(string_len(film->name) + 1);
    array[1] = (char *) malloc(4 + 1);
    array[2] = (char *) malloc(3 + 1);
    array[3] = (char *) malloc(string_len(film->country) + 1);
    array[4] = (char *) malloc(string_len(film->genres) + 1);
    array[5] = (char *) malloc(string_len(film->description) + 1);
    for (size_t i = 0; i < 6; i++) {
        if (NULL == array[i]) {
            exit(77001);
        }
    }
    // добавление в файл: запись в массив записываемых полей
    for (size_t i = 0; i < string_len(film->name); i++) {
        array[0][i] = film->name[i];
    } array[0][string_len(film->name)] = '\0';
    sprintf(array[1], "%4d", film->year); array[1][4] = '\0';
    sprintf(array[2], "%1.1f", film->rating); array[2][3] = '\0';
    for (size_t i = 0; i < string_len(film->country); i++) {
        array[3][i] = film->country[i];
    } array[3][string_len(film->country)] = '\0';
    for (size_t i = 0; i < string_len(film->genres); i++) {
        array[4][i] = film->genres[i];
    } array[4][string_len(film->genres)] = '\0';
    for (size_t i = 0; i < string_len(film->description); i++) {
        array[5][i] = film->description[i];
    } array[5][string_len(film->description)] = '\0';
    // запись в файл
    char *file_name = concatenation(session->login, "_films.csv");
    char *path = concatenation(session->working_dir, file_name);
    cvs_add(path, 6, array);
    // Освобождение памяти
    for (size_t i = 0; i < 6; i++) {
        free(array[i]);
    }
    free(array);
    free(file_name);
    free(path);
}

void change_user_info(struct session *session) {
    // Изменяет информацию о пользователе <login> в списках и в файле пользователей на новую из session
    // удаление старой информации из списков (и из памяти ПК)
    list_remove_user(session->users_list, session->login, true);
    // Выделение памяти под новые данные
    char *login = (char *) malloc(string_len(session->login) + 1);
    char *card = (char *) malloc(string_len(session->card) + 1);
    char *pass = (char *) malloc(string_len(session->pass) + 1);
    if (NULL == login || NULL == card || NULL == pass) {
        exit(77001);
    }
    // Запись данных в новую память
    for (size_t i = 0; i < string_len(session->login); i++) {
        login[i] = session->login[i];
    } login[string_len(session->login)] = '\0';
    for (size_t i = 0; i < string_len(session->card); i++) {
        card[i] = session->card[i];
    } login[string_len(session->card)] = '\0';
    for (size_t i = 0; i < string_len(session->pass); i++) {
        pass[i] = session->pass[i];
    } login[string_len(session->pass)] = '\0';
    // Добавление новых данных в список
    void *data = data_user_create(login, card, pass, session->is_admin);
    list_add(session->users_list, data);
    // запись в файл
    struct user user;
    user.login = session->login;
    user.pass = session->pass;
    user.card = session->card;
    user.is_admin = session->is_admin;
    char *path = concatenation(session->working_dir, "users.csv");
    csv_edit_user(path, &user);
    free(path);
}

void add_film(struct session *session, struct film *film) {
    // Добавляет фильм в список фильмов и в файл фильмов
    if (NULL == session || NULL == film) {
        exit(77004);
    }
    // добавление в текущие списки
    void *data = data_film_create(film->name, film->year, film->rating, film->country, film->genres, film->description);
    list_add(session->films_list, data);
    // добавление в файл: выделение памяти для массива полей
    char **array = (char **) malloc(sizeof(char *) * 6);
    if (NULL == array) {
        exit(77001);
    }
    array[0] = (char *) malloc(string_len(film->name) + 1);
    array[1] = (char *) malloc(4 + 1);
    array[2] = (char *) malloc(3 + 1);
    array[3] = (char *) malloc(string_len(film->country) + 1);
    array[4] = (char *) malloc(string_len(film->genres) + 1);
    array[5] = (char *) malloc(string_len(film->description) + 1);
    for (size_t i = 0; i < 6; i++) {
        if (NULL == array[i]) {
            exit(77001);
        }
    }
    // добавление в файл: запись в массив записываемых полей
    for (size_t i = 0; i < string_len(film->name); i++) {
        array[0][i] = film->name[i];
    } array[0][string_len(film->name)] = '\0';
    sprintf(array[1], "%4d", film->year); array[1][4] = '\0';
    sprintf(array[2], "%1.1f", film->rating); array[2][3] = '\0';
    for (size_t i = 0; i < string_len(film->country); i++) {
        array[3][i] = film->country[i];
    } array[3][string_len(film->country)] = '\0';
    for (size_t i = 0; i < string_len(film->genres); i++) {
        array[4][i] = film->genres[i];
    } array[4][string_len(film->genres)] = '\0';
    for (size_t i = 0; i < string_len(film->description); i++) {
        array[5][i] = film->description[i];
    } array[5][string_len(film->description)] = '\0';
    // запись в файл
    char *path = concatenation(session->working_dir, "films.csv");
    cvs_add(path, 6, array);
    // освобождение памяти
    for (size_t i = 0; i < 6; i++) {
        free(array[i]);
    }
    free(array);
    free(path);
}

void remove_film(struct session *session, char *film_name) {
    // Удаляет фильм из всех списков и из всех файлов
    if (list_film_exists(session->user_favorites_list, film_name)) {
        list_remove_film(session->user_favorites_list, film_name, false);
    }
    list_remove_film(session->films_list, film_name, true);
    // удаление фильма из файлов
    struct dirent *directory_entry;
    DIR *dir = opendir(session->working_dir);
    if (dir == NULL) {
        exit(77013);
    }
    while ((directory_entry = readdir(dir)) != NULL) {
        if (is_strings_ends(directory_entry->d_name, "films.csv")) {
            char *path = concatenation(session->working_dir, directory_entry->d_name);
            cvs_remove(path, film_name);
            free(path);
        }
    }
    closedir(dir);
}

void log_out(struct session *session) {
    // Очищает память и сбрасывает до NULL указатели в session, чтобы начать заново.
    free(session->login); session->login = NULL;
    free(session->card); session->card = NULL;
    free(session->pass); session->pass = NULL;
    session->is_admin = false;
    list_clear(session->user_favorites_list); session->user_favorites_list = NULL;
}

uint8_t screen_start() {
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_start(button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 2;
                        break;
                    case 2:
                        button = 3;
                        break;
                    case 3:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 2:
                        next_screen = 5;
                        flag = false;
                        break;
                    case 3:
                        next_screen = 2;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_registration_login(struct session *session) {
    char *login_buf = (char *) malloc(21);
    if (NULL == login_buf) {
        exit(77001);
    }
    int tmp_buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_registration_login(button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        login_buf[tmp_buf_size] = '\0';
                        if (string_len(login_buf) > 3 && !list_user_exists(session->users_list, login_buf)) {
                            session->login = login_buf;
                            next_screen = 3;
                            flag = false;
                        } else {
                            print_error_login_busy();
                            tmp_buf_size = 0;
                        }
                        break;
                    case 1:
                        next_screen = 1;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (tmp_buf_size == 20) {
                    // пользователь пытается ввести логин длиннее 20 символов
                    print_error_login_too_long();
                    tmp_buf_size = 0;
                }
                login_buf[tmp_buf_size] = pressed_button;
                tmp_buf_size += 1;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_registration_card(struct session *session) {
    char *card_buf = (char *) malloc(17);
    if (NULL == card_buf) {
        exit(77001);
    }
    int buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_registration_card(session->login, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        card_buf[buf_size] = '\0';
                        if (!is_card_valid(card_buf)) {
                            print_error_card();
                        } else {
                            session->card = card_buf;
                            next_screen = 4;
                            flag = false;
                        }
                        break;
                    case 1:
                        next_screen = 2;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (buf_size == 16) {
                    // пользователь пытается ввести карту длиннее 16 символов
                    print_error_card();
                    buf_size = 0;
                }
                card_buf[buf_size] = pressed_button;
                buf_size += 1;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_registration_pass(struct session *session) {
    char *pass_buf = (char *) malloc(101);
    if (NULL == pass_buf) {
        exit(77001);
    }
    int buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_registration_pass(session->login, session->card, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        pass_buf[buf_size] = '\0';
                        buf_size += 1;
                        if (!is_pass_valid(pass_buf)) {
                            // пользователь слабый пароль
                            print_error_weak_pass();
                            buf_size = 0;
                        } else {
                            char *pass = (char *) malloc(buf_size);
                            if (NULL == pass) {
                                exit(77001);
                            }
                            for (size_t i = 0; i < buf_size; i++) {
                                pass[i] = pass_buf[i];
                            }
                            pass[buf_size] = '\0';
                            session->pass = pass;
                            create_user(session);
                            next_screen = 7;
                            flag = false;
                        }
                        break;
                    case 1:
                        next_screen = 3;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (buf_size == 100) {
                    // пользователь пытается ввести пароль длиннее 100 символов
                    print_error_pass_too_long();
                    buf_size = 0;
                }
                pass_buf[buf_size] = pressed_button;
                buf_size += 1;
                break;
        }
    }
    free(pass_buf);
    return next_screen;
}

uint8_t screen_sign_in_login(struct session *session) {
    char *login_buf = (char *) malloc(21);
    if (NULL == login_buf) {
        exit(77001);
    }
    int tmp_buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_sign_in_login(button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        login_buf[tmp_buf_size] = '\0';
                        if (list_user_exists(session->users_list, login_buf)) {
                            session->login = login_buf;
                            next_screen = 6;
                            flag = false;
                        } else {
                            print_error_login_absent(login_buf);
                            tmp_buf_size = 0;
                        }
                        break;
                    case 1:
                        next_screen = 1;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (tmp_buf_size == 20) {
                    // пользователь пытается ввести логин длиннее 20 символов
                    print_error_login_too_long();
                    tmp_buf_size = 0;
                }
                login_buf[tmp_buf_size] = pressed_button;
                tmp_buf_size += 1;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_sign_in_pass(struct session *session) {
    char *tmp_buf = (char *) malloc(101);
    if (NULL == tmp_buf) {
        exit(77001);
    }
    int tmp_buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_sign_in_pass(session->login, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        tmp_buf[tmp_buf_size] = '\0';
                        char *pass_from_list = list_get_pass_by_login(session->users_list, session->login);
                        if (is_strings_equal(tmp_buf, pass_from_list)) {
                            // Добавление информации в session
                            // выделение памяти для полей сессии
                            char *card_from_list = list_get_card_by_login(session->users_list, session->login);
                            char *card = malloc(string_len(card_from_list) + 1);
                            char *pass = malloc(string_len(pass_from_list) + 1);
                            if (NULL == card || NULL == pass) {
                                exit(77001);
                            }
                            // Запись в память полей сессии
                            for (size_t i = 0; i < string_len(card_from_list); i++) {
                                card[i] = card_from_list[i];
                            }
                            card[string_len(card_from_list)] = '\0';
                            for (size_t i = 0; i < string_len(pass_from_list); i++) {
                                pass[i] = pass_from_list[i];
                            }
                            pass[string_len(pass_from_list)] = '\0';
                            // Добавление в сессию
                            session->card = card;
                            session->pass = pass;
                            session->is_admin = list_get_is_admin_by_login(session->users_list, session->login);
                            // Считывание списка избранных фильмов.
                            char *favorites_list_file_name = concatenation(session->login, "_films.csv");
                            char *favorites_list_path = concatenation(session->working_dir, favorites_list_file_name);
                            session->user_favorites_list = cvs_read_films(favorites_list_path);
                            free(favorites_list_file_name);
                            free(favorites_list_path);
                            next_screen = 7;
                            flag = false;
                        } else {
                            print_incorrect_pass();
                            tmp_buf_size = 0;
                        }
                        break;
                    case 1:
                        next_screen = 1;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                if (tmp_buf_size == 100) {
                    // пользователь пытается ввести пароль длиннее 100 символов
                    print_error_pass_too_long();
                    tmp_buf_size = 0;
                }
                tmp_buf[tmp_buf_size] = pressed_button;
                tmp_buf_size += 1;
                break;
        }
    }
    free(tmp_buf);
    return next_screen;
}

uint8_t screen_main(struct session *session) {
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        if (session->films_list->size == 0) {
            print_error_empty_carousel();
            log_out(session);
            next_screen = 1;
            break;
        }
        bool is_favorite = list_film_exists(session->user_favorites_list,
                                            ((struct film*) list_get_offset(session->films_list, 0))->name);
        print_main(session->login, list_get_offset(session->films_list, -1),
                   list_get_offset(session->films_list, 0),
                   list_get_offset(session->films_list, 1), is_favorite, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 6;
                        break;
                    case 6:
                        button = 7;
                        break;
                    case 7:
                        button = 5;
                        break;
                    case 5:
                        button = 4;
                        break;
                    case 4:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 6: // from\to_favorites
                        if (is_favorite) {
                            from_favorites(session, list_get_offset(session->films_list, 0));
                        } else {
                            to_favorites(session, list_get_offset(session->films_list, 0));
                        }
                        break;
                    case 7: // description
                        next_screen = 9;
                        flag = false;
                        break;
                    case 5: // favorites
                        next_screen = 8;
                        flag = false;
                        break;
                    case 4: // profile
                        if (session->is_admin) {
                            next_screen = 11;
                        } else {
                            next_screen = 10;
                        }
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (pressed_button == 'd' || pressed_button == 'D') {
                    list_move(session->films_list, 1);
                } else if (pressed_button == 'a' || pressed_button == 'A') {
                    list_move(session->films_list, -1);
                }
                break;
        }
    }
    return next_screen;
}

uint8_t screen_favorites(struct session *session) {
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        if (session->user_favorites_list->size == 0) {
            print_error_empty_carousel();
            next_screen = 7;
            break;
        }
        print_favorites(session->login, list_get_offset(session->user_favorites_list, -1),
                        list_get_offset(session->user_favorites_list, 0),
                        list_get_offset(session->user_favorites_list, 1), button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 6;
                        break;
                    case 6:
                        button = 7;
                        break;
                    case 7:
                        button = 1;
                        break;
                    case 1:
                        button = 4;
                        break;
                    case 4:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 6: // from favorites
                        from_favorites(session, list_get_offset(session->user_favorites_list, 0));
                        break;
                    case 7: // description
                        next_screen = 9;
                        flag = false;
                        break;
                    case 4: // profile
                        if (session->is_admin) {
                            next_screen = 11;
                        } else {
                            next_screen = 10;
                        }
                        flag = false;
                        break;
                    case 1:
                        next_screen = 7;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (pressed_button == 'd' || pressed_button == 'D') {
                    list_move(session->user_favorites_list, 1);
                } else if (pressed_button == 'a' || pressed_button == 'A') {
                    list_move(session->user_favorites_list, -1);
                }
                break;
        }
    }
    return next_screen;
}

uint8_t screen_description(struct session *session) {
    struct film *film;
    bool is_favorite;
    if (session->prev_screen_out_settings == 7) {
        // main
        film = list_get_offset(session->films_list, 0);
        is_favorite = list_film_exists(session->user_favorites_list, film->name);
    } else if (session->prev_screen_out_settings == 8) {
        // favorites
        film = list_get_offset(session->user_favorites_list, 0);
        is_favorite = true;
    } else {
        exit(77000);
    }
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_description(film, is_favorite, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 6;
                        break;
                    case 6:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 6:
                        if (is_favorite) {
                            from_favorites(session, film);
                            is_favorite = false;
                        } else {
                            to_favorites(session, film);
                            is_favorite = true;
                        }

                        break;
                    case 1:
                        next_screen = 7;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_profile(struct session *session) {
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_profile(session->login, session->card, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 8;
                        break;
                    case 8:
                        button = 9;
                        break;
                    case 9:
                        button = 12;
                        break;
                    case 12:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 8:
                        next_screen = 13;
                        flag = false;
                        break;
                    case 9:
                        next_screen = 12;
                        flag = false;
                        break;
                    case 12:
                        log_out(session);
                        next_screen = 1;
                        flag = false;
                        break;
                    case 1:
                        next_screen = session->prev_screen_out_settings;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_profile_admin(struct session *session) {
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_profile_admin(session->login, session->card, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 8;
                        break;
                    case 8:
                        button = 9;
                        break;
                    case 9:
                        button = 10;
                        break;
                    case 10:
                        button = 11;
                        break;
                    case 11:
                        button = 12;
                        break;
                    case 12:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 8:
                        next_screen = 13;
                        flag = false;
                        break;
                    case 9:
                        next_screen = 12;
                        flag = false;
                        break;
                    case 10:
                        next_screen = 15;
                        flag = false;
                        break;
                    case 11:
                        next_screen = 14;
                        flag = false;
                        break;
                    case 12:
                        log_out(session);
                        next_screen = 1;
                        flag = false;
                        break;
                    case 1:
                        next_screen = session->prev_screen_out_settings;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_change_card(struct session *session) {
    char *card_buf = (char *) malloc(17);
    if (NULL == card_buf) {
        exit(77001);
    }
    int buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_change_card(session->login, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        card_buf[buf_size] = '\0';
                        if (!is_card_valid(card_buf)) {
                            print_error_card();
                        } else {
                            free(session->card);
                            session->card = card_buf;
                            change_user_info(session);
                            if (session->is_admin) {
                                next_screen = 11;
                            } else {
                                next_screen = 10;
                            }
                            flag = false;
                        }
                        break;
                    case 1:
                        if (session->is_admin) {
                            next_screen = 11;
                        } else {
                            next_screen = 10;
                        }
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (buf_size == 16) {
                    // пользователь пытается ввести карту длиннее 16 символов
                    print_error_card();
                    buf_size = 0;
                }
                card_buf[buf_size] = pressed_button;
                buf_size += 1;
                break;
        }
    }
    return next_screen;
}

uint8_t screen_change_pass(struct session *session) {
    char *pass_buf = (char *) malloc(101);
    if (NULL == pass_buf) {
        exit(77001);
    }
    int buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_change_pass(session->login, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        pass_buf[buf_size] = '\0';
                        buf_size += 1;
                        if (!is_pass_valid(pass_buf)) {
                            // пользователь слабый пароль
                            print_error_weak_pass();
                            buf_size = 0;
                        } else {
                            free(session->pass);
                            char *pass = (char *) malloc(buf_size);
                            if (NULL == pass) {
                                exit(77001);
                            }
                            for (size_t i = 0; i < buf_size; i++) {
                                pass[i] = pass_buf[i];
                            }
                            session->pass = pass;
                            change_user_info(session);
                            if (session->is_admin) {
                                next_screen = 11;
                            } else {
                                next_screen = 10;
                            }
                            flag = false;
                        }
                        break;
                    case 1:
                        if (session->is_admin) {
                            next_screen = 11;
                        } else {
                            next_screen = 10;
                        }
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (buf_size == 100) {
                    // пользователь пытается ввести пароль длиннее 100 символов
                    print_error_pass_too_long();
                    buf_size = 0;
                }
                pass_buf[buf_size] = pressed_button;
                buf_size += 1;
                break;
        }
    }
    free(pass_buf);
    return next_screen;
}

uint8_t screen_remove_film(struct session *session) {
    char *film_buf = (char *) malloc(101);
    if (NULL == film_buf) {
        exit(77001);
    }
    int buf_size = 0;
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_remove_film(session->login, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        film_buf[buf_size] = '\0';
                        buf_size += 1;
                        if (!list_film_exists(session->films_list, film_buf)) {
                            print_error_film();
                            buf_size = 0;
                        } else {
                            remove_film(session, film_buf);
                            next_screen = 11;
                            flag = false;
                        }
                        break;
                    case 1:
                        if (session->is_admin) {
                            next_screen = 11;
                        } else {
                            next_screen = 10;
                        }
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (buf_size == 100) {
                    // пользователь пытается ввести фильм длиннее 100 символов
                    print_error_film_too_long();
                    buf_size = 0;
                }
                film_buf[buf_size] = pressed_button;
                buf_size += 1;
                break;
        }
    }
    free(film_buf);
    return next_screen;
}

uint8_t screen_add_film(struct session *session) {
    char *tmp_buf = (char *) malloc(1001);
    size_t buf_size = 0;
    if (NULL == tmp_buf) {
        exit(77001);
    }
    struct film film;
    film.name = NULL;
    film.year = -1;
    film.rating = -1;
    film.country = NULL;
    film.genres = NULL;
    film.description = NULL;
    char *next_field = "name";
    uint8_t next_screen = 0;
    uint8_t button = 0;
    bool flag = true;
    while (flag) {
        print_add_film(session->login, next_field, button);
        char pressed_button = input();
        switch (pressed_button) {
            case '\t':
                switch (button) {
                    case 0:
                        button = 1;
                        break;
                    case 1:
                        button = 0;
                        break;
                    default:
                        button = 0;
                }
                break;
            case '\n':
                switch (button) {
                    case 0:
                        // Обработка поля фильма
                        tmp_buf[buf_size] = '\0';
                        buf_size += 1;
                        if (NULL == film.name) {
                            film.name = (char *) malloc(buf_size + 1);
                            if (NULL == film.name) {
                                exit(77001);
                            }
                            for (size_t i = 0; i < buf_size; i++) {
                                film.name[i] = tmp_buf[i];
                            }
                            film.name[buf_size] = '\0';
                            next_field = "year";
                        } else if (-1 == film.year) {
                            film.year = atoi(tmp_buf);
                            next_field = "rating";
                        } else if (-1 == film.rating) {
                            film.rating = (float) atof(tmp_buf);
                            next_field = "country";
                        } else if (NULL == film.country) {
                            film.country = (char *) malloc(buf_size + 1);
                            if (NULL == film.country) {
                                exit(77001);
                            }
                            for (size_t i = 0; i < buf_size; i++) {
                                film.country[i] = tmp_buf[i];
                            }
                            film.country[buf_size] = '\0';
                            next_field = "genres";
                        } else if (NULL == film.genres) {
                            film.genres = (char *) malloc(buf_size + 1);
                            if (NULL == film.genres) {
                                exit(77001);
                            }
                            for (size_t i = 0; i < buf_size; i++) {
                                film.genres[i] = tmp_buf[i];
                            }
                            film.genres[buf_size] = '\0';
                            next_field = "description";
                        } else if (NULL == film.description) {
                            film.description = (char *) malloc(buf_size + 1);
                            if (NULL == film.description) {
                                exit(77001);
                            }
                            for (size_t i = 0; i < buf_size; i++) {
                                film.description[i] = tmp_buf[i];
                            }
                            film.description[buf_size] = '\0';
                            // добавление информации в список и файл
                            add_film(session, &film);
                            next_screen = 11;
                            flag = false;
                        }
                        buf_size = 0;
                        break;
                    case 1:
                        next_screen = 11;
                        flag = false;
                        break;
                    default:
                        break;
                }
                button = 0;
                break;
            default:
                button = 0;
                if (buf_size == 1000) {
                    // пользователь пытается ввести поле длиннее 1000 символов
                    print_error_field_too_long();
                    buf_size = 0;
                }
                tmp_buf[buf_size] = pressed_button;
                buf_size += 1;
                break;
        }
    }
    free(tmp_buf);
    return next_screen;
}


int main() {
    // Переключение на UTF-8 для Windows
    #ifdef _WIN32
        SetConsoleOutputCP(CP_UTF8);
    #endif
    print_logo();
    sleep(1);
    // начало программы
    struct session session;
    session.login = NULL;
    session.card = NULL;
    session.pass = NULL;
    session.is_admin = false;
    // TODO Change to "../"
    session.working_dir = "../";
    session.user_favorites_list = NULL;
    session.prev_screen_out_settings = 0;
    // Считывание списков фильмов и пользователей
    char *films_path = concatenation(session.working_dir, "films.csv");
    char *users_path = concatenation(session.working_dir, "users.csv");
    session.films_list = cvs_read_films(films_path);
    session.users_list = cvs_read_users(users_path);
    free(films_path);
    free(users_path);
    // Переключение экранов
    uint8_t screen = 1;
    bool flag = true;
    while (flag) {
        switch (screen) {
            case 0: // logo. Прощание
                print_logo();
                flag = false;
                session.prev_screen_out_settings = 0;
                break;
            case 1: //start
                screen = screen_start();
                session.prev_screen_out_settings = 1;
                break;
            case 2: //registration_login
                screen = screen_registration_login(&session);
                session.prev_screen_out_settings = 2;
                break;
            case 3: //registration_card
                screen = screen_registration_card(&session);
                session.prev_screen_out_settings = 3;
                break;
            case 4: //registration_pass
                screen = screen_registration_pass(&session);
                session.prev_screen_out_settings = 4;
                break;
            case 5: //sign_in_login
                screen = screen_sign_in_login(&session);
                session.prev_screen_out_settings = 5;
                break;
            case 6: //sign_in_pass
                screen = screen_sign_in_pass(&session);
                session.prev_screen_out_settings = 6;
                break;
            case 7: //main
                screen = screen_main(&session);
                session.prev_screen_out_settings = 7;
                break;
            case 8: //favorites
                screen = screen_favorites(&session);
                session.prev_screen_out_settings = 8;
                break;
            case 9: //description
                screen = screen_description(&session);
                session.prev_screen_out_settings = 9;
                break;
            case 10: //profile
                screen = screen_profile(&session);
                break;
            case 11: //profile_admin
                screen = screen_profile_admin(&session);
                break;
            case 12: //change_card
                screen = screen_change_card(&session);
                break;
            case 13: //change_pass
                screen = screen_change_pass(&session);
                break;
            case 14: //remove_film
                screen = screen_remove_film(&session);
                break;
            case 15: //add_film
                screen = screen_add_film(&session);
                break;
            default:
                screen = 0;
        }
    }
    return 0;
}