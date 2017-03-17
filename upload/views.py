import simplejson as json
import os, sys
import time
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from db.models import *
from .models import *

# Create your views here.
class UploadView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        user = request.user
        genomes = [x[0] + " | " + x[1] for x in IndexedGenome.objects.values_list('name', 'assembly_id')]
        libraries = [x[0] + " | " + x[1] for x in PreyLibrary.objects.values_list('name', 'feature')]
        if user.submitter.is_omniscient():
            all_baits = Bait.objects.all().values_list('name', flat=True)
            all_vec = Vector.objects.all().values_list('name', flat=True)
            if request.GET['upload_type'] == "bait":
                return render(request, 'upload/upload_super_baits.html', {'genomes': genomes, 'libraries': libraries,
                                                                          'baits': all_baits, 'vectors': all_vec})
            elif request.GET['upload_type'] == 'vector':
                return render(request, 'upload/upload_super_vector.html', {'genomes': genomes, 'libraries': libraries,
                                                                           'baits'  : all_baits, 'vectors': all_vec
                                                                           })
        else:
            baits = user.submitter.get_allowed_baits().values_list('name', flat=True)
            vectors = user.submitter.get_allowed_vectors().values_list('name', flat=True)
            all_vec = Vector.objects.all().values_list('name', flat=True)
            return render(request, 'upload/upload_user.html', {'genomes': genomes, 'libraries': libraries,
                                                               'baits': baits, 'vectors': vectors,
                                                               'all_vectors': all_vec})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        print request.POST
        upload = Upload(user=request.user)
        upload.save()
        for key in request.FILES.keys():
            try:
                bait = Bait.objects.filter(name=key)[0]
                p = request.POST[key + '_prey'].split('|')
                prey_args = {'name': p[0].strip(), 'feature': p[1].strip()}
                prey = PreyLibrary.objects.filter(**prey_args)[0]
                g = request.POST[key + '_genome'].split('|')
                g_args = {'name': g[0].strip(), 'assembly_id': g[1].strip()}
                genome = IndexedGenome.objects.filter(**g_args)[0]
                vector = Vector.objects.filter(name=request.POST[key + '_vector'])[0]
                bait_fil = File(file=request.FILES[key],
                                upload=upload,
                                type='B',
                                bait=bait,
                                vector=vector,
                                prey_library=prey,
                                indexed_genome=genome)
                bait_fil.save()
                request.user.submitter.remove_bait_relation(bait)
            except IndexError:
                p = request.POST[key + '_prey'].split('|')
                prey_args = {'name': p[0].strip(), 'feature': p[1].strip()}
                prey = PreyLibrary.objects.filter(**prey_args)[0]
                g = request.POST[key + '_genome'].split('|')
                g_args = {'name': g[0].strip(), 'assembly_id': g[1].strip()}
                genome = IndexedGenome.objects.filter(**g_args)[0]
                vector = Vector.objects.filter(name=key)[0]
                vect_fil = File(file=request.FILES[key],
                                upload=upload,
                                type='V',
                                vector=vector,
                                prey_library=prey,
                                indexed_genome=genome)
                vect_fil.save()
                request.user.submitter.remove_vector_relation(vector)
        return render(request, 'upload/finished.html')

class FileUpload():
    def __init__(self):
        self.user = None
        self.upload_date = None
        self.files = []

class PendingView(View):
    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)
        self.uploads = {}
        files = File.objects.all()
        for fi in files:
            try:
                self.uploads[fi.upload.id].files.append(fi)
            except KeyError:
                self.uploads[fi.upload.id] = FileUpload()
                self.uploads[fi.upload.id].user = fi.upload.user
                self.uploads[fi.upload.id].date = fi.upload.date
                self.uploads[fi.upload.id].files.append(fi)

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        print self.uploads
        return render(request, 'upload/pending.html', {'uploads': self.uploads})

# except Exception as e:
        #     print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
        #     upload.delete()


        # experiment_name = ''
        # try:
        #     data = request.POST['data'] #.replace("'", "\"")
        #     json_data = json.loads(data)
        #     experiment_name = request.POST['experiment_name']
        #     indexed_genome = IndexedGenome.objects.filter(name=request.POST['indexed_genome'].split(":")[0])[0]
        #     prey_library = PreyLibrary.objects.filter(name=request.POST['prey_library'].split(":")[0])[0]
        #     bait = Bait.objects.filter(name=request.POST['bait'])[0]
        #     vector = Vector.objects.filter(name=request.POST['vector'])[0]
        #     files = json_data['files']
        #     exp = Experiment(name=experiment_name,
        #                      threshold=files['threshold'],
        #                      user=request.user,
        #                      project_name=request.user.submitter.project_name,
        #                      indexed_genome=indexed_genome,
        #                      prey_library=prey_library,
        #                      bait=bait,
        #                      vector=vector,
        #                      bait_selected_filename=files['selected']['bait'],
        #                      bait_non_selected_filename=files['non_selected']['bait'],
        #                      base_selected_filename=files['selected']['vector1'],
        #                      base_non_selected_filename=files['non_selected']['vector1'],
        #                      vector_selected_filename=files['selected']['vector2'],
        #                      vector_non_selected_filename=files['non_selected']['vector2'])
        #     exp.save()
        #     for gene in json_data['genes']:
        #         stats = json_data['genes'][gene]['stats']
        #         enr = Enrichment(gene_name=gene,
        #                          experiment=exp,
        #                          base_ppm=stats[0],
        #                          vector_ppm=stats[1],
        #                          bait_ppm=stats[2],
        #                          value=stats[3],
        #                          adj_value=stats[4],
        #                          p_value=stats[5])
        #         enr.save()
        #
        #         bait_selected_junctions_stats = json_data['genes'][gene]['selected']['bait']['stats']
        #         sjs = SelectedJunctionStat(in_frame_orf=bait_selected_junctions_stats[0],
        #                                    upstream=bait_selected_junctions_stats[1],
        #                                    in_orf=bait_selected_junctions_stats[2],
        #                                    downstream=bait_selected_junctions_stats[3],
        #                                    in_frame=bait_selected_junctions_stats[4],
        #                                    backwards=bait_selected_junctions_stats[5],
        #                                    intron=bait_selected_junctions_stats[6],
        #                                    experiment=exp,
        #                                    enrichment=enr)
        #         sjs.save()
        #
        #         bait_non_selected_junctions_stats = json_data['genes'][gene]['non_selected']['bait']['stats']
        #         nsjs = NonSelectedJunctionStat(in_frame_orf=bait_non_selected_junctions_stats[0],
        #                                        upstream=bait_non_selected_junctions_stats[1],
        #                                        in_orf=bait_non_selected_junctions_stats[2],
        #                                        downstream=bait_non_selected_junctions_stats[3],
        #                                        in_frame=bait_non_selected_junctions_stats[4],
        #                                        backwards=bait_non_selected_junctions_stats[5],
        #                                        intron=bait_non_selected_junctions_stats[6],
        #                                        experiment=exp,
        #                                        enrichment=enr)
        #         nsjs.save()
        #
        #         bait_selected_junctions = json_data['genes'][gene]['selected']['bait']['junctions']
        #         bait_non_selected_junctions = json_data['genes'][gene]['non_selected']['bait']['junctions']
        #
        #         for nm1 in bait_selected_junctions:
        #             for junction1 in bait_selected_junctions[nm1]:
        #                 orf = 'O'
        #                 if int(junction1[4]) == 1:
        #                     orf = 'U'
        #                 elif int(junction1[4]) == 3:
        #                     orf = 'D'
        #
        #                 frame = 'N'
        #                 if int(junction1[3]) == 1:
        #                     frame = 'F'
        #                 elif int(junction1[3]) == 2:
        #                     frame = 'B'
        #                 elif int(junction1[3]) == 3:
        #                     frame = 'I'
        #
        #                 seljunc = SelectedJunction(accession_id=nm1,
        #                                            position=junction1[0],
        #                                            query_start=junction1[1],
        #                                            ppm=junction1[2],
        #                                            frame=frame,
        #                                            orf=orf,
        #                                            gene_name=gene,
        #                                            experiment=exp,
        #                                            enrichment=enr)
        #                 seljunc.save()
        #
        #         for nm2 in bait_non_selected_junctions:
        #             for junction2 in bait_non_selected_junctions[nm2]:
        #                 orf = 'O'
        #                 if int(junction2[4]) == 1:
        #                     orf = 'U'
        #                 elif int(junction2[4]) == 3:
        #                     orf = 'D'
        #
        #                 frame = 'N'
        #                 if int(junction1[3]) == 1:
        #                     frame = 'F'
        #                 elif int(junction1[3]) == 2:
        #                     frame = 'B'
        #                 elif int(junction1[3]) == 3:
        #                     frame = 'I'
        #
        #                 nseljunc = NonSelectedJunction(accession_id=nm2,
        #                                                position=junction2[0],
        #                                                query_start=junction2[1],
        #                                                ppm=junction2[2],
        #                                                frame=frame,
        #                                                orf=orf,
        #                                                gene_name=gene,
        #                                                experiment=exp,
        #                                                enrichment=enr)
        #                 nseljunc.save()
        #
        #     # form = StatMakerForm(request.POST, request.FILES)
        #     # if form.is_valid():
        #     #     f = form.save()
        #     #     fh = open(f.file.url)
        #     #     files = []
        #     #     count = 0
        #     #     for line in fh.readlines():
        #     #         files.append(line.rstrip())
        #     #         count += 1
        #     #         if count > 5:
        #     #             break
        #     #     data = {'is_valid': True, 'name': f.file.name, 'url': f.file.url, 'list': files}
        #     # else:
        #     #     data = {'is_valid': False}
        #     return render(request, 'upload/finished.html', {'experiment': experiment_name, 'error': 0})
        # except Exception as e:
        #     print '%s (%s)' % (e.message, type(e))
        #     err = Error(experiment=experiment_name)
        #     err.save()
