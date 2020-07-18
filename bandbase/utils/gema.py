from app import app

import utils.filters as filters
import utils.fdfgen as fdfgen

import os
import subprocess

def evalfile(path):

    with open(path, 'r') as file:

        return eval(file.read())

def score_gema_type_filter(value):

    if not value: return None

    id = value.ID

    if    id == 1: return 'P' # Potpourri
    elif  id == 2: return 'F' # Werkfragment
    else: raise ValueError('Unsupported GEMA score type ID {0}!'.format(id))

def get_musikfolge_data(gig, dict):

    data = []

    data.extend([
        (dict['Veranstaltung']['Name'],          gig.Name or ''),
        (dict['Veranstaltung']['Art'],           gig.EventNature or ''),
        (dict['Veranstaltung']['Datum'],         filters.datetuple(*gig.DateTuple)),
        (dict['Veranstaltung']['Uhrzeit'],       filters.timetuple(*gig.TimeTuple)),
        (dict['Veranstaltung']['Eintrittsgeld'], gig.EntranceFee or ''),
        (dict['Veranstaltungsort']['Raum'],      gig.EventRoom or '')])

    if gig.AudienceSize and gig.AudienceSize < 10:

        data.append((dict['Veranstaltung']['Zuhoereranzahl'], 1))

    data.extend([
        (dict['Band']['Name'],            gig.SetlistMeta.BandName or ''),
        (dict['Band']['Leiter'],          gig.SetlistMeta.BandLeader.Name or ''),
        (dict['Band']['Mitgliedsnummer'], gig.SetlistMeta.GemaMembershipNumber or ''),
        (dict['Band']['Personenanzahl'],  gig.MusicianCount or ''),
        (dict['Band']['Besetzung'],       gig.LineupKind or ''),
        (dict['Band']['Strasse/Nr'],      '{0} {1}'.format(
                                          gig.SetlistMeta.BandLeader.Street or '',
                                          gig.SetlistMeta.BandLeader.HouseNumber or '')),
        (dict['Band']['PLZ/Ort'],         '{0} {1}'.format(
                                          gig.SetlistMeta.BandLeader.PostalCode or '',
                                          gig.SetlistMeta.BandLeader.City or '')),
        (dict['Band']['Telefon'],         gig.SetlistMeta.BandLeader.LandlinePhone or ''),
        (dict['Band']['Telefax'],         gig.SetlistMeta.BandLeader.Fax or ''),
        (dict['Band']['Mobil'],           gig.SetlistMeta.BandLeader.MobilePhone or ''),
        (dict['Band']['E-Mail'],          gig.SetlistMeta.BandLeader.EMail or ''),
        (dict['Band']['Internetseite'],   gig.SetlistMeta.BandLeader.WWW or '')])

    if gig.GemaType:

        # The expected field value seems to be identical with database entry id
        data.append((dict['Band']['Auswahl'], gig.GemaTypeID))

    if gig.Host:

        data.extend([
            (dict['Veranstalter']['Name'],          gig.Host.Name or ''),
            (dict['Veranstalter']['Strasse/Nr'],    '{0} {1}'.format(
                                                    gig.Host.Street or '',
                                                    gig.Host.HouseNumber or '')),
            (dict['Veranstalter']['PLZ/Ort'],       '{0} {1}'.format(
                                                    gig.Host.PostalCode or '',
                                                    gig.Host.City or '')),
            (dict['Veranstalter']['Telefon'],       gig.Host.LandlinePhone or ''),
            (dict['Veranstalter']['Telefax'],       gig.Host.Fax or ''),
            (dict['Veranstalter']['Mobil'],         gig.Host.MobilePhone or ''),
            (dict['Veranstalter']['E-Mail'],        gig.Host.EMail or ''),
            (dict['Veranstalter']['Internetseite'], gig.Host.WWW or '')])

    if gig.Location:

        data.extend([
            (dict['Veranstaltungsort']['Name'],       gig.Location.Name or ''),
            (dict['Veranstaltungsort']['Art'],        gig.Location.Category.Name or ''),
            (dict['Veranstaltungsort']['Strasse/Nr'], '{0} {1}'.format(
                                                      gig.Location.Street or '',
                                                      gig.Location.HouseNumber or '')),
            (dict['Veranstaltungsort']['PLZ/Ort'],    '{0} {1}'.format(
                                                      gig.Location.PostalCode or '',
                                                      gig.Location.City or ''))])

    if gig.SetlistMeta.GemaCustomerNumber:

        data.extend([(x, gig.SetlistMeta.GemaCustomerNumber)
                    for x in dict['Kundennummer']])

    order = 0

    for gig_score in gig.Scores:

        score = gig_score.Score

        # don't use the native score order,
        # because it may contains an empty
        # placeholder, indicating a pause...
        # order = gig_score.ScoreOrder

        composers = []
        arrangers = []

        for score_person in score.Persons:

            if score_person.IsComposer:
                composers.append(str(score_person.Person))

            if score_person.IsArranger:
                arrangers.append(str(score_person.Person))

        data.extend([
            (dict['Musikstueck'][order]['GEMA-Werk-Nr'], score.GemaWorkNumber or ''),
            (dict['Musikstueck'][order]['P/F'],          score_gema_type_filter(score.GemaType) or ''),
            (dict['Musikstueck'][order]['Titel'],        score.Name or ''),
            (dict['Musikstueck'][order]['Komponist'],    ', '.join(composers)),
            (dict['Musikstueck'][order]['Bearbeiter'],   ', '.join(arrangers)),
            (dict['Musikstueck'][order]['Verleger'],     str(score.Publisher)
                                                         if score.Publisher else '')])

        order += 1

        if order >= 33: break;

    engrosser_flags = [ gig.SetlistMeta.EngrosserSignaturePlace, filters.date(gig.SetlistMeta.EngrosserSignatureDate) ]

    data.append(
    (
        dict['Ausfertigungsvermerk']['Ausfertiger']['Ort/Datum'],
        ', '.join(x for x in engrosser_flags if x)
    ))

    return data

def make_musikfolge_fdf(gig):

    cache_dirname = os.path.join(app.config['SETLIST_CACHE'], str(int(gig)))

    template_path = app.config['SETLIST_TEMPLATE']
    template_dirname = os.path.dirname(template_path)
    template_filename = os.path.basename(template_path)
    template_filename = os.path.splitext(template_filename)[0]

    fdf_filename = template_filename + '.fdf'
    fdf_path = os.path.join(cache_dirname, fdf_filename)

    dict_filename = template_filename + '.py'
    dict_path = os.path.join(template_dirname, dict_filename)

    if not os.path.exists(template_path):
        raise ValueError('Template file "{0}" not found!'.format(template_path))

    if not os.path.exists(dict_path):
        raise ValueError('Dictionary file "{0}" not found!'.format(dict_path))

    if not os.path.exists(cache_dirname):
        os.makedirs(cache_dirname)

    dict = evalfile(dict_path)
    data = get_musikfolge_data(gig, dict)
    fdf_data = fdfgen.forge_fdf(fdf_data_strings=data)

    with open(fdf_path, 'wb') as fdf_file:
        fdf_file.write(fdf_data)

    return fdf_path

def make_musikfolge_pdf(gig, flatten=False):

    fdf_path = make_musikfolge_fdf(gig)

    cache_dirname = os.path.join(app.config['SETLIST_CACHE'], str(int(gig)))

    template_path = app.config['SETLIST_TEMPLATE']
    template_filename = os.path.basename(template_path)
    template_filename = os.path.splitext(template_filename)[0]

    pdf_filename = template_filename + '.pdf'
    pdf_path = os.path.join(cache_dirname, pdf_filename)

    if not os.path.exists(template_path):
        raise ValueError('Template file "{0}" not found!'.format(template_path))

    if not os.path.exists(fdf_path):
        raise ValueError('FDF file "{0}" not found!'.format(fdf_path))

    if not os.path.exists(cache_dirname):
        os.makedirs(cache_dirname)

    args = \
    [
        'pdftk', template_path,
        'fill_form', fdf_path,
        'output', pdf_path
    ]

    if flatten: args.append('flatten')

    try:

        subprocess.check_output(args, stderr=subprocess.STDOUT)

        return pdf_path

    except subprocess.CalledProcessError as e:

        raise ValueError('{0}\n$({1})'.format(
            str(e.output).strip(), ' '.join(args)))
