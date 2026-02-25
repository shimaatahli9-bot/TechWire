let currentTab = 'new';
let currentPage = 1;
let currentArticle = '';
let currentLang = localStorage.getItem('lang') || 'ar';

const translations = {
    ar: {
        fetch: 'جلب الأخبار',
        new_news: 'أخبار جديدة',
        approved: 'تمت الموافقة',
        rejected: 'مرفوضة',
        loading: 'جاري التحميل...',
        no_news: 'لا توجد أخبار',
        write_article: 'كتابة الخبر',
        reject: 'رفض',
        view_article: 'عرض المقال الكامل',
        restore: 'استعادة',
        settings_saved: 'تم حفظ الإعدادات',
        article_created: 'تم إنشاء المقال بنجاح',
        article_failed: 'فشل في إنشاء المقال',
        news_rejected: 'تم رفض الخبر',
        news_restored: 'تم استعادة الخبر',
        news_fetched: 'تم جلب',
        new_article: 'خبر جديد',
        fill_fields: 'يرجى ملء جميع الحقول',
        source_added: 'تم إضافة المصدر',
        source_deleted: 'تم حذف المصدر',
        last_update: 'آخر تحديث',
        ago_now: 'الآن',
        ago_minute: 'منذ',
        ago_minutes: 'دقيقة',
        ago_hour: 'منذ',
        ago_hours: 'ساعة',
        ago_day: 'منذ',
        ago_days: 'يوم',
        load_error: 'خطأ في التحميل',
        delete_confirm: 'هل تريد حذف هذا المصدر؟',
        copied: 'تم نسخ المقال'
    },
    en: {
        fetch: 'Fetch News',
        new_news: 'New News',
        approved: 'Approved',
        rejected: 'Rejected',
        loading: 'Loading...',
        no_news: 'No news available',
        write_article: 'Write Article',
        reject: 'Reject',
        view_article: 'View Full Article',
        restore: 'Restore',
        settings_saved: 'Settings saved',
        article_created: 'Article created successfully',
        article_failed: 'Failed to create article',
        news_rejected: 'News rejected',
        news_restored: 'News restored',
        news_fetched: 'Fetched',
        new_article: 'new article(s)',
        fill_fields: 'Please fill all fields',
        source_added: 'Source added',
        source_deleted: 'Source deleted',
        last_update: 'Last update',
        ago_now: 'now',
        ago_minute: '1 minute ago',
        ago_minutes: 'minutes ago',
        ago_hour: '1 hour ago',
        ago_hours: 'hours ago',
        ago_day: '1 day ago',
        ago_days: 'days ago',
        load_error: 'Loading error',
        delete_confirm: 'Delete this source?',
        copied: 'Article copied'
    },
    fr: {
        fetch: 'Actualiser',
        new_news: 'Nouvelles',
        approved: 'Approuvés',
        rejected: 'Rejetés',
        loading: 'Chargement...',
        no_news: 'Pas de nouvelles',
        write_article: 'Écrire l\'article',
        reject: 'Rejeter',
        view_article: 'Voir l\'article complet',
        restore: 'Restaurer',
        settings_saved: 'Paramètres enregistrés',
        article_created: 'Article créé avec succès',
        article_failed: 'Échec de la création',
        news_rejected: 'Actualité rejetée',
        news_restored: 'Actualité restaurée',
        news_fetched: 'Récupéré',
        new_article: 'nouveau(x) article(s)',
        fill_fields: 'Veuillez remplir tous les champs',
        source_added: 'Source ajoutée',
        source_deleted: 'Source supprimée',
        last_update: 'Dernière mise à jour',
        ago_now: 'maintenant',
        ago_minute: 'il y a 1 minute',
        ago_minutes: 'minutes',
        ago_hour: 'il y a 1 heure',
        ago_hours: 'heures',
        ago_day: 'il y a 1 jour',
        ago_days: 'jours',
        load_error: 'Erreur de chargement',
        delete_confirm: 'Supprimer cette source?',
        copied: 'Article copié'
    },
    es: {
        fetch: 'Obtener noticias',
        new_news: 'Nuevas',
        approved: 'Aprobadas',
        rejected: 'Rechazadas',
        loading: 'Cargando...',
        no_news: 'Sin noticias',
        write_article: 'Escribir artículo',
        reject: 'Rechazar',
        view_article: 'Ver artículo completo',
        restore: 'Restaurar',
        settings_saved: 'Configuración guardada',
        article_created: 'Artículo creado con éxito',
        article_failed: 'Error al crear artículo',
        news_rejected: 'Noticia rechazada',
        news_restored: 'Noticia restaurada',
        news_fetched: 'Obtenido',
        new_article: 'nuevo(s) artículo(s)',
        fill_fields: 'Por favor complete todos los campos',
        source_added: 'Fuente agregada',
        source_deleted: 'Fuente eliminada',
        last_update: 'Última actualización',
        ago_now: 'ahora',
        ago_minute: 'hace 1 minuto',
        ago_minutes: 'minutos',
        ago_hour: 'hace 1 hora',
        ago_hours: 'horas',
        ago_day: 'hace 1 día',
        ago_days: 'días',
        load_error: 'Error de carga',
        delete_confirm: '¿Eliminar esta fuente?',
        copied: 'Artículo copiado'
    },
    de: {
        fetch: 'Nachrichten laden',
        new_news: 'Neu',
        approved: 'Genehmigt',
        rejected: 'Abgelehnt',
        loading: 'Laden...',
        no_news: 'Keine Nachrichten',
        write_article: 'Artikel schreiben',
        reject: 'Ablehnen',
        view_article: 'Vollständigen Artikel anzeigen',
        restore: 'Wiederherstellen',
        settings_saved: 'Einstellungen gespeichert',
        article_created: 'Artikel erfolgreich erstellt',
        article_failed: 'Fehler beim Erstellen',
        news_rejected: 'Nachricht abgelehnt',
        news_restored: 'Nachricht wiederhergestellt',
        news_fetched: 'Geladen',
        new_article: 'neue(r) Artikel',
        fill_fields: 'Bitte alle Felder ausfüllen',
        source_added: 'Quelle hinzugefügt',
        source_deleted: 'Quelle gelöscht',
        last_update: 'Letzte Aktualisierung',
        ago_now: 'jetzt',
        ago_minute: 'vor 1 Minute',
        ago_minutes: 'Minuten',
        ago_hour: 'vor 1 Stunde',
        ago_hours: 'Stunden',
        ago_day: 'vor 1 Tag',
        ago_days: 'Tagen',
        load_error: 'Ladefehler',
        delete_confirm: 'Diese Quelle löschen?',
        copied: 'Artikel kopiert'
    },
    tr: {
        fetch: 'Haberleri Getir',
        new_news: 'Yeni',
        approved: 'Onaylanan',
        rejected: 'Reddedilen',
        loading: 'Yükleniyor...',
        no_news: 'Haber yok',
        write_article: 'Makale Yaz',
        reject: 'Reddet',
        view_article: 'Tam Makaleyi Gör',
        restore: 'Geri Yükle',
        settings_saved: 'Ayarlar kaydedildi',
        article_created: 'Makale başarıyla oluşturuldu',
        article_failed: 'Makale oluşturulamadı',
        news_rejected: 'Haber reddedildi',
        news_restored: 'Haber geri yüklendi',
        news_fetched: 'Getirildi',
        new_article: 'yeni makale',
        fill_fields: 'Lütfen tüm alanları doldurun',
        source_added: 'Kaynak eklendi',
        source_deleted: 'Kaynak silindi',
        last_update: 'Son güncelleme',
        ago_now: 'şimdi',
        ago_minute: '1 dakika önce',
        ago_minutes: 'dakika önce',
        ago_hour: '1 saat önce',
        ago_hours: 'saat önce',
        ago_day: '1 gün önce',
        ago_days: 'gün önce',
        load_error: 'Yükleme hatası',
        delete_confirm: 'Bu kaynak silinsin mi?',
        copied: 'Makale kopyalandı'
    }
};

function t(key) {
    return translations[currentLang][key] || translations['ar'][key] || key;
}

async function api(endpoint, options = {}) {
    const res = await fetch(endpoint, options);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg transform transition-all z-50 ${type === 'success' ? 'bg-pink-700' : 'bg-red-600'} text-white`;
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';
    setTimeout(() => {
        toast.style.transform = 'translateY(100%)';
        toast.style.opacity = '0';
    }, 3000);
}

function timeAgo(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    if (diff < 60) return t('ago_now');
    if (diff < 3600) return `${t('ago_minute')} ${Math.floor(diff / 60)} ${t('ago_minutes')}`;
    if (diff < 86400) return `${t('ago_hour')} ${Math.floor(diff / 3600)} ${t('ago_hours')}`;
    return `${t('ago_day')} ${Math.floor(diff / 86400)} ${t('ago_days')}`;
}

async function loadCounts() {
    const counts = await api('/api/news/counts');
    document.getElementById('count-new').textContent = counts.new || 0;
    document.getElementById('count-approved').textContent = counts.approved || 0;
    document.getElementById('count-rejected').textContent = counts.rejected || 0;
}

async function loadNews() {
    const container = document.getElementById('news-container');
    const loading = document.getElementById('loading');
    container.innerHTML = '';
    loading.classList.remove('hidden');
    
    try {
        const data = await api(`/api/news?status=${currentTab}&page=${currentPage}`);
        loading.classList.add('hidden');
        
        if (data.news.length === 0) {
            container.innerHTML = `<div class="text-center text-pink-500 py-10 card-bg rounded-xl">${t('no_news')}</div>`;
            return;
        }
        
        data.news.forEach(item => {
            container.appendChild(createNewsCard(item));
        });
    } catch (e) {
        loading.classList.add('hidden');
        container.innerHTML = `<div class="text-center text-red-500 py-10 card-bg rounded-xl">${t('load_error')}: ${e.message}</div>`;
    }
}

function createNewsCard(item) {
    const card = document.createElement('div');
    card.className = 'card-bg rounded-xl shadow-md p-4 card-enter border border-pink-100';
    card.id = `news-${item.id}`;
    
    if (currentTab === 'new') {
        card.innerHTML = `
            <div class="flex items-center gap-2 mb-2">
                <span class="bg-pink-100 text-pink-700 text-xs px-2 py-1 rounded-full">${item.category}</span>
                <span class="text-pink-500 text-sm">${item.source_name}</span>
                <span class="text-pink-400 text-sm mr-auto">${timeAgo(item.fetched_at)}</span>
            </div>
            <h3 class="text-lg font-bold text-gray-800 mb-2">${item.title_ar}</h3>
            <p class="text-gray-600 text-sm mb-4 line-clamp-3">${item.summary_ar}</p>
            <div class="flex gap-2">
                <button onclick="approveNews('${item.id}')" class="flex-1 btn-primary text-white py-2 rounded-lg transition flex items-center justify-center gap-2 shadow-md">
                    ✅ ${t('write_article')}
                </button>
                <button onclick="rejectNews('${item.id}')" class="flex-1 bg-pink-100 text-pink-700 py-2 rounded-lg hover:bg-pink-200 transition">
                    ❌ ${t('reject')}
                </button>
            </div>
        `;
    } else if (currentTab === 'approved') {
        const preview = item.article_ar ? item.article_ar.substring(0, 100) + '...' : '';
        card.innerHTML = `
            <div class="flex items-center gap-2 mb-2">
                <span class="bg-green-100 text-green-600 text-xs px-2 py-1 rounded-full">${item.category}</span>
                <span class="text-pink-500 text-sm">${item.source_name}</span>
                <span class="text-pink-400 text-sm mr-auto">${timeAgo(item.fetched_at)}</span>
            </div>
            <h3 class="text-lg font-bold text-gray-800 mb-2">${item.title_ar}</h3>
            <p class="text-gray-600 text-sm mb-4">${preview}</p>
            <button onclick="showArticle('${item.id}')" class="w-full bg-pink-100 text-pink-700 py-2 rounded-lg hover:bg-pink-200 transition">
                ${t('view_article')}
            </button>
        `;
    } else {
        card.innerHTML = `
            <div class="flex items-center justify-between">
                <div>
                    <span class="text-pink-500 text-sm">${item.source_name}</span>
                    <h3 class="text-gray-600">${item.title_ar}</h3>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-pink-400 text-sm">${timeAgo(item.fetched_at)}</span>
                    <button onclick="restoreNews('${item.id}')" class="text-pink-600 hover:text-pink-800 text-sm">${t('restore')}</button>
                </div>
            </div>
        `;
    }
    
    return card;
}

async function approveNews(id) {
    const card = document.getElementById(`news-${id}`);
    const btn = card.querySelector('button');
    const titleEl = card.querySelector('h3');
    const title = titleEl ? titleEl.textContent : '';
    btn.innerHTML = '<div class="spinner mx-auto"></div>';
    btn.disabled = true;
    
    try {
        const data = await api(`/api/news/${id}/approve`, { method: 'POST' });
        if (data.success) {
            currentArticle = data.article;
            showModal(title, data.article);
            card.classList.add('card-exit');
            setTimeout(() => {
                loadNews();
                loadCounts();
            }, 300);
            showToast(t('article_created'));
        }
    } catch (e) {
        btn.innerHTML = `✅ ${t('write_article')}`;
        btn.disabled = false;
        showToast(t('article_failed'), 'error');
    }
}

async function rejectNews(id) {
    const card = document.getElementById(`news-${id}`);
    card.classList.add('card-exit');
    
    try {
        await api(`/api/news/${id}/reject`, { method: 'POST' });
        setTimeout(() => {
            loadNews();
            loadCounts();
        }, 300);
        showToast(t('news_rejected'));
    } catch (e) {
        card.classList.remove('card-exit');
        showToast(t('news_rejected'), 'error');
    }
}

async function restoreNews(id) {
    try {
        await api(`/api/news/${id}/restore`, { method: 'POST' });
        loadNews();
        loadCounts();
        showToast(t('news_restored'));
    } catch (e) {
        showToast(t('news_restored'), 'error');
    }
}

async function showArticle(id) {
    const data = await api(`/api/news?status=approved`);
    const item = data.news.find(n => n.id === id);
    if (item) {
        currentArticle = item.article_ar;
        showModal(item.title_ar, item.article_ar);
    }
}

function showModal(title, content) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-content').textContent = content;
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal(e) {
    if (!e || e.target.id === 'modal-overlay') {
        document.getElementById('modal-overlay').classList.add('hidden');
    }
}

function copyArticle() {
    navigator.clipboard.writeText(currentArticle).then(() => {
        showToast(t('copied'));
    });
}

function switchTab(tab) {
    currentTab = tab;
    currentPage = 1;
    document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.remove('tab-active'));
    document.getElementById(`tab-${tab}`).classList.add('tab-active');
    loadNews();
}

async function fetchNews() {
    const btn = event.target.closest('button');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="spinner mx-auto"></div>';
    btn.disabled = true;
    
    try {
        const data = await api('/api/news/fetch', { method: 'POST' });
        btn.innerHTML = originalText;
        btn.disabled = false;
        loadNews();
        loadCounts();
        showToast(`${t('news_fetched')} ${data.new_count} ${t('new_article')}`);
    } catch (e) {
        btn.innerHTML = originalText;
        btn.disabled = false;
        showToast(t('news_fetched'), 'error');
    }
}

function toggleSettings() {
    const sidebar = document.getElementById('settings-sidebar');
    const isRtl = currentLang === 'ar';
    sidebar.classList.toggle(isRtl ? '-translate-x-full' : 'translate-x-full');
    if (!sidebar.classList.contains(isRtl ? '-translate-x-full' : 'translate-x-full')) {
        loadSettings();
        loadSources();
    }
}

async function loadSettings() {
    const settings = await api('/api/settings');
    if (settings.fetch_interval_minutes) {
        document.getElementById('fetch-interval').value = settings.fetch_interval_minutes;
    }
    if (settings.max_news_age_hours) {
        document.getElementById('max-age').value = settings.max_news_age_hours;
    }
}

async function updateSettings() {
    const settings = {
        fetch_interval_minutes: document.getElementById('fetch-interval').value,
        max_news_age_hours: document.getElementById('max-age').value
    };
    await api('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ settings })
    });
    showToast(t('settings_saved'));
}

async function loadSources() {
    const data = await api('/api/sources');
    const container = document.getElementById('sources-list');
    container.innerHTML = data.sources.map(s => `
        <div class="flex items-center justify-between bg-pink-50 rounded-lg px-3 py-2 border border-pink-100">
            <span class="text-sm ${s.enabled ? 'text-gray-700' : 'text-gray-400'}">${s.name}</span>
            <div class="flex items-center gap-2">
                <label class="relative inline-flex cursor-pointer">
                    <input type="checkbox" ${s.enabled ? 'checked' : ''} onchange="toggleSource(${s.id}, this.checked)" class="sr-only peer">
                    <div class="w-9 h-5 bg-gray-300 peer-checked:bg-pink-600 rounded-full peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:right-0.5 after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all"></div>
                </label>
                <button onclick="deleteSource(${s.id})" class="text-red-500 hover:text-red-700">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
            </div>
        </div>
    `).join('');
}

async function toggleSource(id, enabled) {
    await api(`/api/sources/${id}?enabled=${enabled}`, { method: 'PUT' });
}

async function deleteSource(id) {
    if (confirm(t('delete_confirm'))) {
        await api(`/api/sources/${id}`, { method: 'DELETE' });
        loadSources();
        showToast(t('source_deleted'));
    }
}

async function addNewSource() {
    const name = document.getElementById('new-source-name').value.trim();
    const url = document.getElementById('new-source-url').value.trim();
    
    if (!name || !url) {
        showToast(t('fill_fields'), 'error');
        return;
    }
    
    await api('/api/sources', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, url })
    });
    
    document.getElementById('new-source-name').value = '';
    document.getElementById('new-source-url').value = '';
    loadSources();
    showToast(t('source_added'));
}

async function init() {
    await loadCounts();
    await loadNews();
    
    const settings = await api('/api/settings');
    if (settings.last_fetch_time) {
        document.getElementById('last-update').textContent = `${t('last_update')}: ${timeAgo(settings.last_fetch_time)}`;
    }
}

init();
